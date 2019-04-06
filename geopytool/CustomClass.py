version = '0.8.19.4.104'

date = '2019-4-6'

dpi = 128
#coding:utf-8

from geopytool.ImportDependence import *

#from geopytool.TableViewer import TableViewer


class GrowingTextEdit(QtWidgets.QTextEdit):

    def __init__(self, *args, **kwargs):
        super(GrowingTextEdit, self).__init__(*args, **kwargs)
        self.document().contentsChanged.connect(self.sizeChange)

        self.heightMin = 0
        self.heightMax = 8

    def sizeChange(self):
        docHeight = self.document().size().height()
        if self.heightMin <= docHeight <= self.heightMax:
            self.setMinimumHeight(docHeight)

class Tool():
    def TriToBin(self, x, y, z):

        '''
        Turn an x-y-z triangular coord to an a-b coord.
        if z is negative, calc with its abs then return (a, -b).
        :param x,y,z: the three numbers of the triangular coord
        :type x,y,z: float or double are both OK, just numbers
        :return:  the corresponding a-b coord
        :rtype:   a tuple consist of a and b
        '''

        if (z >= 0):
            if (x + y + z == 0):
                return (0, 0)
            else:
                Sum = x + y + z
                X = 100.0 * x / Sum
                Y = 100.0 * y / Sum
                Z = 100.0 * z / Sum
                if (X + Y != 0):
                    a = Z / 2.0 + (100.0 - Z) * Y / (Y + X)
                else:
                    a = Z / 2.0
                b = Z / 2.0 * (np.sqrt(3))
                return (a, b)
        else:
            z = abs(z)
            if (x + y + z == 0):
                return (0, 0)
            else:
                Sum = x + y + z
                X = 100.0 * x / Sum
                Y = 100.0 * y / Sum
                Z = 100.0 * z / Sum
                if (X + Y != 0):
                    a = Z / 2.0 + (100.0 - Z) * Y / (Y + X)
                else:
                    a = Z / 2.0
                b = Z / 2.0 * (np.sqrt(3))
                return (a, -b)

    def BinToTri(self, a, b):

        '''
        Turn an a-b coord to an x-y-z triangular coord .
        if z is negative, calc with its abs then return (a, -b).
        :param a,b: the numbers of the a-b coord
        :type a,b: float or double are both OK, just numbers
        :return:  the corresponding x-y-z triangular coord
        :rtype:   a tuple consist of x,y,z
        '''

        if (b >= 0):
            y = a - b / np.sqrt(3)
            z = b * 2 / np.sqrt(3)
            x = 100 - (a + b / np.sqrt(3))
            return (x, y, z)
        else:
            y = a + b / np.sqrt(3)
            z = b * 2 / np.sqrt(3)
            x = 100 - (a - b / np.sqrt(3))
            return (x, y, z)

    def Cross(self, A=[(0, 0), (10, 10)], B=[(0, 10), (100, 0)]):

        '''
        Return the crosspoint of two line A and B.
        :param A: first line
        :type A: a list consist of two tuples, beginning and end point of the line
        :param B: second line
        :type B: a list consist of two tuples, beginning and end point of the line
        :return: the crosspoint of A and B
        :rtype: a list consist of two numbers, the x-y of the crosspoint
        '''

        x0, y0 = A[0]
        x1, y1 = A[1]
        x2, y2 = B[0]
        x3, y3 = B[1]

        b1 = (y1 - y0) / (x1 - x0)
        b2 = (y3 - y2) / (x3 - x2)
        c1 = y0 - b1 * x0
        c2 = y2 - b2 * x2

        x = (c2 - c1) / (b1 - b2)
        y = b1 * x + c1

        return ([x, y])

    def TriCross(self, A=[(100, 0, 0), (0, 50, 60)], B=[(50, 50, 0), (0, 0, 100)]):

        '''
        Return the crosspoint of two line A and B in triangular coord.
        :param A: first line
        :type A: a list consist of two tuples, beginning and end point of the line
        :param B: second line
        :type B: a list consist of two tuples, beginning and end point of the line
        :return:  the crosspoint of A and B
        :rtype:   a list consist of three numbers, the x-y-z of the triangular coord
        '''

        x0, y0 = self.TriToBin(A[0][0], A[0][1], A[0][2])
        x1, y1 = self.TriToBin(A[1][0], A[1][1], A[1][2])
        x2, y2 = self.TriToBin(B[0][0], B[0][1], B[0][2])
        x3, y3 = self.TriToBin(B[1][0], B[1][1], B[1][2])

        b1 = (y1 - y0) / (x1 - x0)
        b2 = (y3 - y2) / (x3 - x2)
        c1 = y0 - b1 * x0
        c2 = y2 - b2 * x2

        x = (c2 - c1) / (b1 - b2)
        y = b1 * x + c1

        result = self.BinToTri(x, y)
        return (result)

    def Fill(self, P=[(100, 0), (85, 15), (0, 3)], Color='blue', Alpha=0.3):

        '''
        Fill a region in planimetric rectangular coord.
        :param P: the peak points of the region in planimetric rectangular coord
        :type P: a list consist of at least three tuples, which are the points in planimetric rectangular coord
        :param Color: the color used to fill the region
        :type Color: a string; b: blue, g: green, r: red, c: cyan, m: magenta, y: yellow, k: black, w: white
        :param Alpha: the transparency used to fill the region
        :type Alpha: a float number from 0 to 1, higher darker, lower more transparent
        '''
        a = []
        b = []

        for i in P:
            a.append(i[0])
            b.append(i[1])

        return (a, b)

    def TriFill(self, P=[(100, 0, 0), (85, 15, 0), (0, 3, 97)], Color='blue', Alpha=0.3):

        '''
         Fill a region in triangular coord.
        :param P: the peak points of the region in triangular coord
        :type P: a list consist of at least three tuples, which are the points in triangular coord
        :param Color: the color used to fill the region
        :type Color: a string; b: blue, g: green, r: red, c: cyan, m: magenta, y: yellow, k: black, w: white
        :param Alpha: the transparency used to fill the region
        :type Alpha: a float number from 0 to 1, higher darker, lower more transparent
        '''

        a = []
        b = []

        for i in P:
            a.append(self.TriToBin(i[0], i[1], i[2])[0])
            b.append(self.TriToBin(i[0], i[1], i[2])[1])

        return (a, b)
        # plt.fill(a, b, Color=Color, Alpha=Alpha, )

class Point():
    '''
    a Point class
    :param X,Y: the values of its x-y coord
    :type X,Y: two float numbers
    :param Location: gather X and Y as a tuple for further use
    :type Location: just a tuple with two numbers
    :param Size: the size of the Point to draw on canvas
    :type Size: a number , int or maybe float also OK , better around 1 to 20, not too large or too small
    :param Color: the color of the Point to draw on canvas
    :type Color: a string; b: blue, g: green, r: red, c: cyan, m: magenta, y: yellow, k: black, w: white
    :param Alpha: the transparency of the Point
    :type Alpha: a float number from 0 to 1, higher darker, lower more transparent
    :param Marker: the marker used for the Point
    :type Marker: a string; o, d, *, ^ , maybe there would be some other types , from matplotlib
    :param Label: label of the Point, telling what it is and distinguish it from other points
    :type Label: a string , if leave as '' or '' such kind of blank string, the label will not show on canvas
    '''

    X = 0
    Y = 0
    Location = (X, Y)
    Size = 12
    Color = 'red'
    Alpha = 0.3
    Marker = 'o'
    Label = ''

    def __init__(self, X=0, Y=0, Size=12, Color='red', Alpha=0.3, Marker='o', Label=''):
        '''
        just set up the values
        '''
        super().__init__()
        self.X = X
        self.Y = Y
        self.Location = (X, Y)
        self.Size = Size
        self.Color = Color
        self.Alpha = Alpha
        self.Marker = Marker
        self.Label = Label

class Points():
    '''
    a class for multiple Points
    :param X,Y: the values of its x-y coords
    :type X,Y: two lists consist of float numbers
    :param Size: the size of the Points to draw on canvas
    :type Size: a number , int or maybe float also OK , better around 1 to 20, not too large or too small
    :param Color: the color of the Points to draw on canvas
    :type Color: a string; b: blue, g: green, r: red, c: cyan, m: magenta, y: yellow, k: black, w: white
    :param Alpha: the transparency of the Points
    :type Alpha: a float number from 0 to 1, higher darker, lower more transparent
    :param Marker: the marker used for the Points
    :type Marker: a string; o, d, *, ^ , maybe there would be some other types , from matplotlib
    :param Label: label of the Points, telling what they are and distinguish them from other points
    :type Label: a string , if leave as '' or '' such kind of blank string, the label will not show on canvas
    '''

    X = []
    Y = []
    # Location = (X, Y)
    Size = 12
    Color = 'red'
    Alpha = 0.3
    Marker = 'o'
    Label = ''
    FontSize = 8

    def __init__(self, points=[(0, 0), (0, 1)], Size=12, Color='red', Alpha=0.3, Marker='o', Label='', FontSize=8):
        '''
        just set up the values
        '''
        super().__init__()
        self.X = []
        self.Y = []
        for i in points:
            self.X.append(i[0])
            self.Y.append(i[1])
        # self.Location = (self.X, self.Y)
        self.Size = Size
        self.Color = Color
        self.Alpha = Alpha
        self.Marker = Marker
        self.Label = Label
        self.FontSize = FontSize

class Tag():
    '''
    a class for Tag put on canvas
    :param Label: label of the Tag, telling what it is and distinguish them from other tags
    :type Label: a strings , if leave as '' or '' such kind of blank string, the label will not show on canvas
    :param Location: the location of the Tag
    :type Location: a tuple consist of x-y values of its coords
    :param X_offset,Y_offset: the values of its x-y offsets on coords
    :type X_offset,Y_offset: two float numbers
    :param FontSize: the size of font of the Tag
    :type FontSize: a number , int or maybe float also OK , better around 8 to 12, not too large or too small
    '''

    Label = u'Label'
    Location = (0, 0)
    X_offset = -6
    Y_offset = 3
    FontSize = 8

    def __init__(self, Label=u'Label', Location=(0, 0), X_offset=-6, Y_offset=3, FontSize=8):
        '''
        set up the values
        '''

        self.Label = Label
        self.Location = Location
        self.X_offset = X_offset
        self.Y_offset = Y_offset
        self.FontSize = FontSize

class Line():
    '''
    a line class
    :param Begin: the Beginning point of the line
    :type Begin: a Point Instance
    :param End: the End point of the line
    :type End: a Point Instance
    :param Points: gathering all the Point Instances
    :type Points: a list
    :param X,Y: the gathered x and y values of the line to use in plotting
    :type X,Y: two lists containing float numbers
    :param Width: the width of the line
    :type Width: an int number , mayby float is OK
    :param Color: the color of the Line to draw on canvas
    :type Color: a string; b: blue, g: green, r: red, c: cyan, m: magenta, y: yellow, k: black, w: white
    :param Style: the style used for the Line
    :type Style: a string; -, --,-., : maybe there would be some other types , from matplotlib
    :param Alpha: the transparency of the Point
    :type Alpha: a float number from 0 to 1, higher darker, lower more transparent
    :param Label: label of the Line, telling what it is and distinguish it from other lines
    :type Label: a string , if leave as '' or '' such kind of blank string, the label will not show on canvas
    :param Sort: the sequence used for sorting the points consisting the line
    :type Sort: a string, x means sort the points with their x values, y means use y instead of x, other means use the sequence of points as these points are put to the line
    '''

    Begin = Point(0, 0)
    End = Point(1, 1)
    Points = []
    X = [Begin.X, End.X]
    Y = [Begin.Y, End.Y]
    Width = 1
    Color = 'blue'
    Style = '-'
    Alpha = 0.3
    Label = ''
    Sort = ''

    def __init__(self, Points=[(0, 0), (1, 1)], Sort='', Width=1, Color='blue', Style='-', Alpha=0.3, Label=''):
        '''
        setup the datas
        '''
        super().__init__()
        self.Sort = Sort
        self.Width = Width
        self.Color = Color
        self.Style = Style
        self.Alpha = Alpha
        self.Label = Label

        if (len(Points) == 2):
            self.X = [Points[0][0], Points[1][0]]
            self.Y = [Points[0][1], Points[1][1]]
            self.Points = Points

        elif (len(Points) > 2):
            self.Points = Points

        else:

            # print('Cannot draw line with one point')
            pass

    def sequence(self):
        '''
        sort the points in the line with given option
        '''
        if (len(self.Points[0]) == 2):
            if (self.Sort == 'X' or self.Sort == 'x'):
                self.Points.sort(key=lambda x: x[0])
                self.order(self.Points)

            elif (self.Sort == 'Y' or self.Sort == 'y'):
                self.Points.sort(key=lambda x: x[1])
                self.order(self.Points)
            else:
                self.order(self.Points)

        if (len(self.Points[0]) == 3):
            if (self.Sort == 'X' or self.Sort == 'x'):
                self.Points.sort(key=lambda x: x[0])
                self.order(self.Points)

            elif (self.Sort == 'Y' or self.Sort == 'y'):
                self.Points.sort(key=lambda x: x[1])
                self.order(self.Points)
            elif (self.Sort == 'Z' or self.Sort == 'Z'):
                self.Points.sort(key=lambda x: x[2])
                self.order(self.Points)
            else:
                self.order(self.Points)

    def order(self, TMP=[]):
        X_TMP = []
        Y_TMP = []
        for i in TMP:
            X_TMP.append(i[0])
            Y_TMP.append(i[1])
        self.X = X_TMP
        self.Y = Y_TMP

class TriTag(Tag, Tool):
    '''
    inherit Tag and Tool,a Tag for triangular coord
    '''

    def __init__(self, Label=u'Label', Location=(0, 1, 2), X_offset=-6, Y_offset=3, FontSize=12):
        '''
        set up the values, transfer x,y,z coords to x-y coords
        '''

        self.Label = Label
        self.Location = self.TriToBin(Location[0], Location[1], Location[2])
        self.X_offset = X_offset
        self.Y_offset = Y_offset
        self.FontSize = FontSize

class TriPoint(Point, Tool):
    '''
    inherit Point and Tool, a Point class for triangular coord
    :param x,y,z: the list for gathering the x,y,z values of points consisting the line
    :type x,y,z: three lists
    :param sum: a value used in calc of coord transfer
    :type sum: just a number, both int or float are OK
    '''
    x = 0
    y = 0
    z = 0
    sum = 1

    def __init__(self, P=(10, 20, 70), Size=12, Color='red', Alpha=0.3, Marker='o', Label=''):
        super().__init__()

        self.sum = P[0] + P[1] + abs(P[2])
        self.x = P[0] * 100 / self.sum
        self.y = P[1] * 100 / self.sum
        self.z = P[2] * 100 / self.sum

        self.Location = P
        self.Size = Size
        self.Color = Color
        self.Alpha = Alpha
        self.Marker = Marker
        self.Label = Label

        self.X, self.Y = self.TriToBin(self.x, self.y, self.z)

class TriLine(Line, Tool):
    '''
    inherit Line and Tool, line class for triangular coord
    :param x,y,z: the list for gathering the x,y,z values of points consisting the line
    :type x,y,z: three lists
    '''
    x = []
    y = []
    z = []

    X = []
    Y = []

    def __init__(self, Points=[(0, 0, 0), (1, 1, 1)], Sort='', Width=1, Color='blue', Style='-', Alpha=0.3, Label=''):
        super().__init__()
        self.Sort = Sort
        self.Width = Width
        self.Color = Color
        self.Style = Style
        self.Alpha = Alpha
        self.Label = Label

        if (len(Points) == 2):

            TriPoint(Points[0])

            self.x = [Points[0][0], Points[1][0]]
            self.y = [Points[0][1], Points[1][1]]
            self.z = [Points[0][2], Points[1][2]]
            self.tritrans()
            self.Points = Points

        elif (len(Points) > 2):
            self.Points = Points

            for i in Points:
                self.x.append(i[0])
                self.y.append(i[1])
                self.z.append(i[2])

        else:
            # print('Cannot draw line with one point')
            pass

        self.sequence()
        self.tritrans()

    def tritrans(self):
        self.X = []
        self.Y = []
        for i in range(len(self.x)):
            self.X.append((self.TriToBin(self.x[i], self.y[i], self.z[i]))[0])
            self.Y.append((self.TriToBin(self.x[i], self.y[i], self.z[i]))[1])

    def order(self, TMP=[]):
        X_TMP = []
        Y_TMP = []
        Z_TMP = []
        for i in TMP:
            X_TMP.append(i[0])
            Y_TMP.append(i[1])
            Z_TMP.append(i[2])
        self.x = X_TMP
        self.y = Y_TMP
        self.z = Z_TMP

class PandasModel(QtCore.QAbstractTableModel):
    _df = pd.DataFrame()
    _changed = False

    def __init__(self, df=pd.DataFrame(), parent=None):
        QtCore.QAbstractTableModel.__init__(self, parent=parent)
        self._df = df
        self._changed = False


        self._filters = {}
        self._sortBy = []
        self._sortDirection = []


    def headerData(self, section, orientation, role=QtCore.Qt.DisplayRole):
        if role != QtCore.Qt.DisplayRole:
            return QtCore.QVariant()

        if orientation == QtCore.Qt.Horizontal:
            try:
                return self._df.columns.tolist()[section]
            except (IndexError,):
                return QtCore.QVariant()
        elif orientation == QtCore.Qt.Vertical:
            try:
                # return self.df.index.tolist()
                return self._df.index.tolist()[section]
            except (IndexError,):
                return QtCore.QVariant()

    def data(self, index, role):
        if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
            try:
                row = index.row()
                col = index.column()
                name = self._struct[col]['name']
                return self._data[row][name]
            except:
                pass
        elif role == QtCore.Qt.CheckStateRole:
            return None

        return QtCore.QVariant(str(self._df.ix[index.row(), index.column()]))

    def flags(self, index):
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable

    '''
    def setData(self, index, value, role=QtCore.Qt.EditRole):
        row = index.row()
        col = index.column()
        name = self._struct[col]['name']
        self._data[row][name] = value
        self.emit(QtCore.SIGNAL('dataChanged()'))
        return True
    '''

    def setData(self, index, value, role=QtCore.Qt.EditRole):
        row = self._df.index[index.row()]
        col = self._df.columns[index.column()]
        if hasattr(value, 'toPyObject'):
            # PyQt4 gets a QVariant
            value = value.toPyObject()
        else:
            # PySide gets an unicode
            dtype = self._df[col].dtype
            if dtype != object:
                value = None if value == '' else dtype.type(value)
        #self._df.set_value(row, col, value)
        self._df.at[row,col]= value
        self._changed = True
        # self.emit(QtCore.SIGNAL('dataChanged()'))
        return True

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self._df.index)

    def columnCount(self, parent=QtCore.QModelIndex()):
        return len(self._df.columns)

    def sort(self, column, order):
        colname = self._df.columns.tolist()[column]

        index = self._df.index.tolist()
        self.layoutAboutToBeChanged.emit()

        #self._df.sort_values(colname, ascending=order == QtCore.Qt.AscendingOrder, inplace=True)
        #self._df.reset_index(inplace=True, drop=True)

        try:
            self._df.sort_values(colname, ascending=order == QtCore.Qt.AscendingOrder, inplace=True)
        except:
            pass
        try:
            self._df.reset_index(inplace=True, drop=True)
        except:
            pass

        self.layoutChanged.emit()

class CustomQTableView(QtWidgets.QTableView):

    df = pd.DataFrame()
    def __init__(self, *args):
        super().__init__(*args)

        self.resize(800, 600)
        self.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers |
                             QtWidgets.QAbstractItemView.DoubleClicked)


    def keyPressEvent(self, event):  # Reimplement the event here
        return

class NewCustomQTableView(QtWidgets.QTableView):

    path=''
    def __init__(self, *args):
        super().__init__(*args)
        self.setAcceptDrops(True)

        self.resize(800, 600)
        self.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers |
                             QtWidgets.QAbstractItemView.DoubleClicked)

    def keyPressEvent(self, event):  # Reimplement the event here
        return


    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            files = [(u.toLocalFile()) for u in event.mimeData().urls()]
            for f in files:
                if 'csv' in f or 'xls' in f:
                    print('Drag', f)
                    self.path=f

                    if ('csv' in f):
                        self.parent().raw = pd.read_csv(f)
                    elif ('xls' in f):
                        self.parent().raw = pd.read_excel(f)

                    # #print(self.raw)


            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        files = [(u.toLocalFile()) for u in event.mimeData().urls()]
        for f in files:
            print('Drop')

class TableViewer(QMainWindow):
    addon = 'Name Author DataType Label Marker Color Size Alpha Style Width TOTAL total LOI loi'

    Minerals = ['Quartz',
                'Zircon',
                'K2SiO3',
                'Anorthite',
                'Na2SiO3',
                'Acmite',
                'Diopside',
                'Sphene',
                'Hypersthene',
                'Albite',
                'Orthoclase',
                'Wollastonite',
                'Olivine',
                'Perovskite',
                'Nepheline',
                'Leucite',
                'Larnite',
                'Kalsilite',
                'Apatite',
                'Halite',
                'Fluorite',
                'Anhydrite',
                'Thenardite',
                'Pyrite',
                'Magnesiochromite',
                'Chromite',
                'Ilmenite',
                'Calcite',
                'Na2CO3',
                'Corundum',
                'Rutile',
                'Magnetite',
                'Hematite',
                'Q',
                'A',
                'P',
                'F', ]

    Calced = ['Fe3+/(Total Fe) in rock',
              'Mg/(Mg+Total Fe) in rock',
              'Mg/(Mg+Fe2+) in rock',
              'Mg/(Mg+Fe2+) in silicates',
              'Ca/(Ca+Na) in rock',
              'Plagioclase An content',
              'Differentiation Index']
    DataWeight = {}
    DataVolume = {}
    DataBase = {}
    DataCalced = {}
    raw = pd.DataFrame()

    result = pd.DataFrame()
    Para = pd.DataFrame()
    _df = pd.DataFrame()
    data_to_test = pd.DataFrame()
    data_to_test_location =''
    begin_result = pd.DataFrame()
    load_result = pd.DataFrame()

    def __init__(self, parent=None, df=pd.DataFrame(), title='Statistical Result'):
        QMainWindow.__init__(self, parent)
        self.setAcceptDrops(True)
        self.setWindowTitle(title)
        self.df = df
        self.create_main_frame()
        self.create_status_bar()

    def Old__init__(self, parent=None, df=pd.DataFrame()):
        QWidget.__init__(self, parent)
        self.setWindowTitle('TAS (total alkali–silica) diagram Volcanic/Intrusive (Wilson et al. 1989)')

        self._df = df
        if (len(df) > 0):
            self._changed = True
            # print('DataFrame recieved to TabelView')

        self.AllLabel = []

        for i in range(len(self._df)):
            tmp_label = self._df.at[i, 'Label']
            if tmp_label not in self.AllLabel:
                self.AllLabel.append(tmp_label)

        for i in range(len(self.LocationAreas)):
            tmpi = self.LocationAreas[i] + [self.LocationAreas[i][0]]
            tmppath = path.Path(tmpi)
            self.AreasHeadClosed.append(tmpi)
            patch = patches.PathPatch(tmppath, facecolor='orange', lw=0.3, alpha=0.3)

            self.SelectDic[self.ItemNames[i]] = tmppath

        self.create_main_frame()
        self.create_status_bar()

    def create_main_frame(self):

        self.resize(800, 600)
        self.main_frame = QWidget()

        self.save_button = QPushButton('&Save')
        self.save_button.clicked.connect(self.saveResult)

        self.tableView = CustomQTableView(self.main_frame)
        self.tableView.setObjectName('tableView')
        self.tableView.setSortingEnabled(True)

        self.vbox = QVBoxLayout()

        self.vbox.addWidget(self.tableView)
        self.vbox.addWidget(self.save_button)

        self.main_frame.setLayout(self.vbox)
        self.setCentralWidget(self.main_frame)

        self.model = PandasModel(self.df)
        self.tableView.setModel(self.model)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        files = [(u.toLocalFile()) for u in event.mimeData().urls()]
        for f in files:
            print(f)

    def clearLayout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.clearLayout(item.layout())

    def resizeEvent(self, evt=None):

        w = self.width()
        h = self.height()
        '''
        if h<=360:
            h=360
            self.resize(w,h)
        if w<=640:
            w = 640
            self.resize(w, h)
        '''

        step = (w * 94 / 100) / 5
        foot = h * 3 / 48

    def ErrorEvent(self, text=''):

        _translate = QtCore.QCoreApplication.translate

        if (text == ''):
            reply = QMessageBox.information(self, _translate('MainWindow', 'Warning'), _translate('MainWindow',
                                                                                                  'Your Data mismatch this Function.\n Some Items missing?\n Or maybe there are blanks in items names?\n Or there are nonnumerical value？'))
        else:
            reply = QMessageBox.information(self, _translate('MainWindow', 'Warning'), _translate('MainWindow',
                                                                                                  'Your Data mismatch this Function.\n Error infor is:') + text)

    def create_main_frame(self):

        self.resize(800, 600)
        self.main_frame = QWidget()

        self.save_button = QPushButton('&Save')
        self.save_button.clicked.connect(self.saveDataFile)

        self.tableView = CustomQTableView(self.main_frame)
        self.tableView.setObjectName('tableView')
        self.tableView.setSortingEnabled(True)


        self.vbox = QVBoxLayout()

        self.vbox.addWidget(self.tableView)
        self.vbox.addWidget(self.save_button)

        self.main_frame.setLayout(self.vbox)
        self.setCentralWidget(self.main_frame)

        self.model = PandasModel(self.df)
        self.tableView.setModel(self.model)


    def create_status_bar(self):
        self.status_text = QLabel("Click Save button to save.")
        self.statusBar().addWidget(self.status_text, 1)

    def add_actions(self, target, actions):
        for action in actions:
            if action is None:
                target.addSeparator()
            else:
                target.addAction(action)

    def saveDataFile(self):

        # if self.model._changed == True:
        # print('changed')
        # print(self.model._df)

        DataFileOutput, ok2 = QFileDialog.getSaveFileName(self,
                                                          '文件保存',
                                                          'C:/',
                                                          'Excel Files (*.xlsx);;CSV Files (*.csv)')  # 数据文件保存输出

        if "Label" in self.model._df.columns.values.tolist():
            self.model._df = self.model._df.set_index('Label')

        if (DataFileOutput != ''):

            if ('csv' in DataFileOutput):
                self.model._df.to_csv(DataFileOutput, sep=',', encoding='utf-8')

            elif ('xls' in DataFileOutput):
                self.model._df.to_excel(DataFileOutput, encoding='utf-8')

    def create_action(self, text, slot=None, shortcut=None,
                      icon=None, tip=None, checkable=False,
                      signal='triggered()'):
        action = QAction(text, self)
        if icon is not None:
            action.setIcon(QIcon(':/%s.png' % icon))
        if shortcut is not None:
            action.setShortcut(shortcut)
        if tip is not None:
            action.setToolTip(tip)
            action.setStatusTip(tip)
        if slot is not None:
            action.triggered.connect(slot)
        if checkable:
            action.setCheckable(True)
        return action

class AppForm(QMainWindow):
    result = pd.DataFrame()
    Para = pd.DataFrame()
    _df = pd.DataFrame()
    _df_back = pd.DataFrame()
    data_to_test = pd.DataFrame()
    data_to_test_location =''
    begin_result = pd.DataFrame()
    load_result = pd.DataFrame()

    kernel_list = ['linear','rbf','sigmoid','poly']
    _changed = False

    xlabel = r'$SiO_2 wt\%$'
    ylabel = r'$Na_2O + K_2O wt\%$'
    reference = 'Print the reference here.'
    AllLabel = []
    IndexList=[]
    LabelList=[]
    ItemNames = ['Foidolite',
                 'Peridotgabbro',
                 'Foid Gabbro',
                 'Foid Monzodiorite',
                 'Foid Monzosyenite',
                 'Foid Syenite',
                 'Gabbro Bs',
                 'Gabbro Ba',
                 'Monzogabbro',
                 'Monzodiorite',
                 'Monzonite',
                 'Syenite',
                 'Quartz Monzonite',
                 'Gabbroic Diorite',
                 'Diorite',
                 'Granodiorite',
                 'Granite',
                 'Quartzolite',
                 ]

    LocationAreas = [[[41, 3], [37, 3], [35, 9], [37, 14], [52.5, 18], [52.5, 14], [48.4, 11.5], [45, 9.4], [41, 7]],
                     [[41, 0], [41, 3], [45, 3], [45, 0]],
                     [[41, 3], [41, 7], [45, 9.4], [49.4, 7.3], [45, 5], [45, 3]],
                     [[45, 9.4], [48.4, 11.5], [53, 9.3], [49.4, 7.3]],
                     [[48.4, 11.5], [52.5, 14], [57.6, 11.7], [53, 9.3]],
                     [[52.5, 14], [52.5, 18], [57, 18], [63, 16.2], [61, 13.5], [57.6, 11.7]],
                     [[45, 0], [45, 2], [52, 5], [52, 0]],
                     [[45, 2], [45, 5], [52, 5]],
                     [[45, 5], [49.4, 7.3], [52, 5]],
                     [[49.4, 7.3], [53, 9.3], [57, 5.9], [52, 5]],
                     [[53, 9.3], [57.6, 11.7], [61, 8.6], [63, 7], [57, 5.9]],
                     [[57.6, 11.7], [61, 13.5], [63, 16.2], [71.8, 13.5], [61, 8.6]],
                     [[61, 8.6], [71.8, 13.5], [69, 8], [63, 7]],
                     [[52, 0], [52, 5], [57, 5.9], [57, 0]],
                     [[57, 0], [57, 5.9], [63, 7], [63, 0]],
                     [[63, 0], [63, 7], [69, 8], [77.3, 0]],
                     [[77.3, 0], [69, 8], [71.8, 13.5], [85.9, 6.8], [87.5, 4.7]],
                     [[77.3, 0], [87.5, 4.7], [90, 4.7], [90, 0]],
                     ]

    AreasHeadClosed = []

    SelectDic = {}

    Standard=''
    FileName_Hint = ''
    WholeResult = {}
    OutPutCheck= True
    OutPutTitle = 'Blank Title'
    OutPutData = pd.DataFrame()
    OutPutFig = Figure((8.0, 8.0))
    itemstocheck = ['SiO2', 'K2O', 'Na2O']

    def __init__(self, parent=None, df=pd.DataFrame()):
        QWidget.__init__(self, parent)
        self.setWindowTitle('TAS (total alkali–silica) diagram Volcanic/Intrusive (Wilson et al. 1989)')
        self.FileName_Hint = ''
        self._df = df
        self._df_back = df
        if (len(df) > 0):
            self._changed = True
            # print('DataFrame recieved to AppForm')

        self.AllLabel=[]

        for i in range(len(self._df)):
            tmp_label = self._df.at[i, 'Label']
            if tmp_label not in self.AllLabel:
                self.AllLabel.append(tmp_label)


        for i in range(len(self.LocationAreas)):
            tmpi = self.LocationAreas[i] + [self.LocationAreas[i][0]]
            tmppath = path.Path(tmpi)
            self.AreasHeadClosed.append(tmpi)
            patch = patches.PathPatch(tmppath, facecolor='orange', lw=0.3, alpha=0.3)

            self.SelectDic[self.ItemNames[i]] = tmppath

        self.create_main_frame()
        self.create_status_bar()

    def CleanDataFile(self,raw=pd.DataFrame(),checklist=['质量','分数','百分比',' ','ppm','ma', 'wt','%','(',')','（','）','[',']','【','】']):


        for i in checklist:
            raw = raw.rename(columns=lambda x: x.replace(i, ''))
            pass

        for i in raw.dtypes.index:
            if raw.dtypes[i] != float and raw.dtypes[i] != int and i not in ['Marker', 'Color', 'Size', 'Alpha', 'Style','Width', 'Label']:
                print(i)
                raw = raw.drop(i, 1)

        for i in raw.columns.values.tolist():
            if i=='':
                raw = raw.drop(i, 1)

        raw = raw.dropna(axis=1, how='all')

        #Columns = raw.columns.values.tolist()
        #Rows = raw.index.values.tolist()

        for i in raw.index.values.tolist():
            if type(raw.at[i, 'Label'])== str:
                if 'tandard' in raw.at[i, 'Label']:
                    print('Your Self Defined Standard is at the line No.', i)
                    self.Standard = raw.loc[i]
                    raw = raw.drop(i)

        raw = raw.reset_index(drop=True)

        return(raw)
        print(raw.columns.values.tolist())

    def Check(self):

        row = self._df.index.tolist()
        col = self._df.columns.tolist()
        itemstocheck = self.itemstocheck
        checklist = list((set(itemstocheck).union(set(col))) ^ (set(itemstocheck) ^ set(col)))
        if len(checklist) == len(itemstocheck):
            self.OutPutCheck = True
        else:
            self.OutPutCheck = False
        return(self.OutPutCheck)

    def clearLayout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.clearLayout(item.layout())

    def resizeEvent(self, evt=None):

        w=self.width()
        h=self.height()
        '''
        if h<=360:
            h=360
            self.resize(w,h)
        if w<=640:
            w = 640
            self.resize(w, h)
        '''


        step = (w * 94 / 100) / 5
        foot=h*3/48

    def OldErrorEvent(self):
        _translate = QtCore.QCoreApplication.translate
        reply = QMessageBox.information(self,  _translate('MainWindow','Warning'),  _translate('MainWindow','Your Data mismatch this Function.\n Some Items missing?\n Or maybe there are blanks in items names?\n Or there are nonnumerical value？'))

    def ErrorEvent(self,text=''):

        _translate = QtCore.QCoreApplication.translate
        
        if(text==''):
            reply = QMessageBox.information(self, _translate('MainWindow', 'Warning'), _translate('MainWindow',
                                                                                                  'Your Data mismatch this Function.\n Some Items missing?\n Or maybe there are blanks in items names?\n Or there are nonnumerical value？'))
        else:
            reply = QMessageBox.information(self, _translate('MainWindow', 'Warning'), _translate('MainWindow',
                                                                                                      'Your Data mismatch this Function.\n Error infor is:') + text)

    def DrawLine(self, l=[(41, 0), (41, 3), (45, 3)], color='grey', linewidth=0.5, linestyle='-', linelabel='',
                 alpha=0.5):
        x = []
        y = []
        for i in l:
            x.append(i[0])
            y.append(i[1])

        self.axes.plot(x, y, color=color, linewidth=linewidth, linestyle=linestyle, label=linelabel, alpha=alpha)
        return (x, y)

    def DrawLogLine(self, l=[(41, 0), (41, 3), (45, 3)], color='grey', linewidth=0.5, linestyle='-', linelabel='',
                    alpha=0.5):
        x = []
        y = []
        for i in l:
            x.append(math.log(i[0], 10))
            y.append(math.log(i[1], 10))

        self.axes.plot(x, y, color=color, linewidth=linewidth, linestyle=linestyle, label=linelabel, alpha=alpha)
        return (x, y)

    def save_plot(self):
        file_choices = 'pdf Files (*.pdf);;SVG Files (*.svg);;PNG Files (*.png)'

        path = QFileDialog.getSaveFileName(self,
                                           'Save file', '',
                                           file_choices)
        if path:
            self.canvas.print_figure(path, dpi=self.dpi)
            self.statusBar().showMessage('Saved to %s' % path, 2000)

    def save_plot_quitely(self,path= '~/',name='Target'):
        self.canvas.print_figure(path + name + '.pdf', dpi=self.dpi)
        self.canvas.print_figure(path + name + '.png', dpi=self.dpi)

    def stateval(self,data=np.ndarray):
        #print(type(data),data)
        dict={'min': min(data),'max': max(data),'median': nanmedian(data), 'mean':nanmean(data), 'ptp':ptp(data), 'var':nanvar(data), 'std':nanstd(data), 'cv':nanmean(data)/nanstd(data)}

        return(dict)

    def create_main_frame(self):
        self.main_frame = QWidget()
        self.dpi = 128
        self.fig = Figure((8.0, 8.0), dpi=self.dpi)
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self.main_frame)
        self.axes = self.fig.add_subplot(111)
        # Create the navigation toolbar, tied to the canvas
        self.mpl_toolbar = NavigationToolbar(self.canvas, self.main_frame)

        # Other GUI controls
        self.save_button = QPushButton('&Save')
        self.save_button.clicked.connect(self.saveImgFile)

        self.draw_button = QPushButton('&Reset')
        self.draw_button.clicked.connect(self.TAS)

        self.legend_cb = QCheckBox('&Legend')
        self.legend_cb.setChecked(True)
        self.legend_cb.stateChanged.connect(self.TAS)  # int

        self.tag_cb = QCheckBox('&Tag')
        self.tag_cb.setChecked(True)
        self.tag_cb.stateChanged.connect(self.TAS)  # int

        self.more_cb = QCheckBox('&More')
        self.more_cb.setChecked(True)
        self.more_cb.stateChanged.connect(self.TAS)  # int

        self.detail_cb = QCheckBox('&Detail')
        self.detail_cb.setChecked(True)
        self.detail_cb.stateChanged.connect(self.TAS)  # int

        slider_label = QLabel('Location:')
        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(1, 5)
        self.slider.setValue(1)
        self.slider.setTracking(True)
        self.slider.setTickPosition(QSlider.TicksBothSides)
        self.slider.valueChanged.connect(self.TAS)  # int

        #
        # Layout with box sizers
        #
        self.hbox = QHBoxLayout()

        for w in [self.save_button, self.draw_button, self.detail_cb, self.tag_cb, self.more_cb,
                  self.legend_cb, slider_label, self.slider]:
            self.hbox.addWidget(w)
            self.hbox.setAlignment(w, Qt.AlignVCenter)

        self.vbox = QVBoxLayout()
        self.vbox.addWidget(self.mpl_toolbar)
        self.vbox.addWidget(self.canvas)
        self.vbox.addLayout(self.hbox)
        self.textbox = GrowingTextEdit(self)
        self.textbox.setText(self.reference)

        self.vbox.addWidget(self.textbox)
        self.main_frame.setLayout(self.vbox)
        self.setCentralWidget(self.main_frame)

    def create_status_bar(self):
        self.status_text = QLabel("Click Save button to save.")
        self.statusBar().addWidget(self.status_text, 1)

    def add_actions(self, target, actions):
        for action in actions:
            if action is None:
                target.addSeparator()
            else:
                target.addAction(action)

    def exportScene(self):
        ImgFileOutput, ok2 = QFileDialog.getSaveFileName(self,
                                                         '文件保存',
                                                         'C:/',
                                                         'PNG Files (*.png)')  # 设置文件扩展名过滤,注意用双分号间隔

        pix = QtWidgets.QWidget.grab(self.canvas)
        #pix.save("./capture.png", "PNG")
        pix.save(ImgFileOutput)

    def OLDsaveImgFile(self):
        ImgFileOutput, ok2 = QFileDialog.getSaveFileName(self,
                                                         '文件保存',
                                                         'C:/',
                                                         'pdf Files (*.pdf);;SVG Files (*.svg);;PNG Files (*.png)')  # 设置文件扩展名过滤,注意用双分号间隔

        if (ImgFileOutput != ''):
            self.canvas.print_figure(ImgFileOutput, dpi=300)
            #self.canvas.print_raw(ImgFileOutput, dpi=300)


    def saveImgFile(self):
        ImgFileOutput, ok2 = QFileDialog.getSaveFileName(self,
                                                         '文件保存',
                                                         'C:/'+self.FileName_Hint,
                                                         'pdf Files (*.pdf);;SVG Files (*.svg);;PNG Files (*.png)')  # 设置文件扩展名过滤,注意用双分号间隔

        if (ImgFileOutput != ''):
            self.canvas.print_figure(ImgFileOutput, dpi=300)
            #self.canvas.print_raw(ImgFileOutput, dpi=300)


    def getDataFiles(self,limit=6):
        print('get Multiple Data Files  called \n')
        DataFilesInput, filetype = QFileDialog.getOpenFileNames(self, u'Choose Data File',
                                                                '~/',
                                                                'Excel Files (*.xlsx);;Excel 2003 Files (*.xls);;CSV Files (*.csv)')  # 设置文件扩展名过滤,注意用双分号间隔
        # print(DataFileInput,filetype)

        DataFramesList = []

        if len(DataFilesInput) >= 1 :
            for i in range(len(DataFilesInput)):
                if i < limit:
                    if ('csv' in DataFilesInput[i]):
                        DataFramesList.append(pd.read_csv(DataFilesInput[i]))
                    elif ('xls' in DataFilesInput[i]):
                        DataFramesList.append(pd.read_excel(DataFilesInput[i]))
                else:
                    #self.ErrorEvent(text='You can only open up to 6 Data Files at a time.')
                    pass

        return(DataFramesList,DataFilesInput)



    def getDataFile(self,CleanOrNot=True):
        _translate = QtCore.QCoreApplication.translate

        DataFileInput, filetype = QFileDialog.getOpenFileName(self,_translate('MainWindow', u'Choose Data File'),
                                                                  '~/',
                                                                  'Excel Files (*.xlsx);;Excel 2003 Files (*.xls);;CSV Files (*.csv)')  # 设置文件扩展名过滤,注意用双分号间隔
        print(DataFileInput)

        raw_input_data=pd.DataFrame()

        if ('csv' in DataFileInput):
            raw_input_data = pd.read_csv(DataFileInput)
        elif ('xls' in DataFileInput):
            raw_input_data = pd.read_excel(DataFileInput)

        if len(raw_input_data)>0:
            return(raw_input_data,DataFileInput)
        else:
            return('Blank')

    def getFileName(self,list=['C:/Users/Fred/Documents/GitHub/Writing/元素数据/Ag.xlsx']):
        result=[]
        for i in list:
            result.append(i.split("/")[-1].split(".")[0])
        print(result)
        return(result)

    def Key_Func(self):
        pass




    def loadDataToTest(self):
        TMP =self.getDataFile()
        if TMP != 'Blank':
            self.data_to_test=TMP[0]
            self.data_to_test_location=TMP[1]
        self.Key_Func()

    def saveDataFile(self):

        # if self.model._changed == True:
        # print('changed')
        # print(self.model._df)

        DataFileOutput, ok2 = QFileDialog.getSaveFileName(self,
                                                          '文件保存',
                                                          'C:/'+self.FileName_Hint,
                                                          'Excel Files (*.xlsx);;CSV Files (*.csv)')  # 数据文件保存输出

        if "Label" in self.model._df.columns.values.tolist():
            self.model._df=self.model._df.set_index('Label')

        if (DataFileOutput != ''):

            if ('csv' in DataFileOutput):
                self.model._df.to_csv(DataFileOutput, sep=',', encoding='utf-8')

            elif ('xls' in DataFileOutput):
                self.model._df.to_excel(DataFileOutput, encoding='utf-8')

    def saveResult(self):

        self.result.reset_index
        DataFileOutput, ok2 = QFileDialog.getSaveFileName(self,
                                                          '文件保存',
                                                          'C:/',
                                                          'Excel Files (*.xlsx);;CSV Files (*.csv)')  # 数据文件保存输出

        if (DataFileOutput != ''):

            if ('csv' in DataFileOutput):

                # DataFileOutput = DataFileOutput[0:-4]

                self.result.to_csv(DataFileOutput, sep=',', encoding='utf-8')
                # self.result.to_csv(DataFileOutput + '.csv', sep=',', encoding='utf-8')

            elif ('xlsx' in DataFileOutput):

                # DataFileOutput = DataFileOutput[0:-5]

                self.result.to_excel(DataFileOutput, encoding='utf-8')

                # self.result.to_excel(DataFileOutput + '.xlsx', encoding='utf-8')

    def savePara(self):

        self.Para.reset_index
        DataFileOutput, ok2 = QFileDialog.getSaveFileName(self,
                                                          '文件保存',
                                                          'C:/',
                                                          'Excel Files (*.xlsx);;CSV Files (*.csv)')  # 数据文件保存输出

        if (DataFileOutput != ''):

            if ('csv' in DataFileOutput):

                # DataFileOutput = DataFileOutput[0:-4]

                self.Para.to_csv(DataFileOutput, sep=',', encoding='utf-8')
                # self.Para.to_csv(DataFileOutput + '.csv', sep=',', encoding='utf-8')

            elif ('xlsx' in DataFileOutput):

                # DataFileOutput = DataFileOutput[0:-5]

                self.Para.to_excel(DataFileOutput, encoding='utf-8')

                # self.Para.to_excel(DataFileOutput + '.xlsx', encoding='utf-8')


    def showResult(self):

        self.result.reset_index

        self.resultpop = TableViewer(df=self.result, title='Results')
        self.resultpop.show()


    def showPara(self):

        self.Para.reset_index

        self.parapop = TableViewer(df=self.Para, title='Parameters')
        self.parapop.show()

    def create_action(self, text, slot=None, shortcut=None,
                      icon=None, tip=None, checkable=False,
                      signal='triggered()'):
        action = QAction(text, self)
        if icon is not None:
            action.setIcon(QIcon(':/%s.png' % icon))
        if shortcut is not None:
            action.setShortcut(shortcut)
        if tip is not None:
            action.setToolTip(tip)
            action.setStatusTip(tip)
        if slot is not None:
            action.triggered.connect(slot)
        if checkable:
            action.setCheckable(True)
        return action

    def GetResult(self):
        self.WholeResult={'Check':True,'Title':self.OutPutTitle,'Data':self.OutPutData,'Fig':self.OutPutFig}
        return(self.WholeResult)

    def DropUseless(self,df= pd.DataFrame(),droplist = ['Q (Mole)', 'A (Mole)', 'P (Mole)', 'F (Mole)',
                    'Q (Mass)', 'A (Mass)', 'P (Mass)', 'F (Mass)']):
        for t in droplist:
            if t in df.columns.values:
                df = df.drop(t, 1)
        return(df)

    def ReduceSize(self,df=pd.DataFrame):

        m = ['Width', 'Style', 'Alpha', 'Size', 'Color', 'Marker', 'Author']

        for i in m:
            if i in df.columns.values:
                df = df.drop(i, 1)
        df = df.loc[:, (df != 0).any(axis=0)]
        return(df)


    def Slim(self,df= pd.DataFrame()):

        ItemsAvalibale = df.columns.values.tolist()
        if 'Label' in ItemsAvalibale:
            df = df.set_index('Label')

        df = df.dropna(axis=1,how='all')

        ItemsToTest = ['Number', 'Tag', 'Name', 'Author', 'DataType', 'Marker', 'Color', 'Size', 'Alpha',
                       'Style', 'Width']

        for i in ItemsToTest:
            if i in ItemsAvalibale:
                df = df.drop(i, 1)

        df = df.apply(pd.to_numeric, errors='coerce')
        df = df.dropna(axis='columns')

        return(df)



    def relation(self,data1=np.ndarray,data2=np.ndarray):
        data=array([data1,data2])
        dict={'cov':cov(data,bias=1),'corrcoef':corrcoef(data)}
        return(dict)

    def Hsim_Distance(self,a=[1,2],b=[5,6,7,8]):
        tmp =[]
        result=0
        for i in range(min(len(a),len(b))):
            tmp.append( 1.0/(1+np.abs(a[i]-b[i])))

        #print(tmp)
        result=np.sum(tmp)/(min([len(a),len(b)]))
        return(result)


    def Close_Distance(self,a=[1,2,3,4],b=[5,6,7,8]):
        tmp =[]
        result=0
        for i in range(min([len(a),len(b)])):
            tmp.append(  np.power(np.e,-np.abs(a[i]-b[i]) )  )

        #print(tmp)
        result=np.sum(tmp)/(min([len(a),len(b)]))
        return(result)




class PlotModel(FigureCanvas):
    _df = pd.DataFrame()
    _changed = False

    def __init__(self, parent=None, width=100, height=100, dpi=100, description=''
                 , tag='', xlabel=r'$X$', ylabel=r'$Y$', xlim=(30, 90), ylim=(0, 20)):

        self.fig = Figure(figsize=(width, height), dpi=dpi)

        self.axes = self.fig.add_subplot(111, xlabel=xlabel + '\n' + description, ylabel=ylabel, xlim=xlim, ylim=ylim)

        FigureCanvas.__init__(self, self.fig)

        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QSizePolicy.Expanding,
                                   QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def DrawLine(self, l=[(41, 0), (41, 3), (45, 3)], color='grey', linewidth=0.5, linestyle='-', linelabel='',
                 alpha=0.5):
        x = []
        y = []
        for i in l:
            x.append(i[0])
            y.append(i[1])

        self.axes.plot(x, y, color=color, linewidth=linewidth, linestyle=linestyle, label=linelabel, alpha=alpha)
        return (x, y)



    def TAS(self, df=pd.DataFrame(), Left=35, Right=79, X0=30, X1=90, X_Gap=7, Base=0,
            Top=19, Y0=1, Y1=19, Y_Gap=19, FontSize=12, xLabel=r'$SiO_2 wt\%$', yLabel=r'$na_2O + K_2O wt\%$'):

        PointLabels = []
        x = []
        y = []

        self.DrawLine([(41, 0), (41, 3), (45, 3)])
        self.DrawLine([(45, 0), (45, 3), (45, 5), (49.4, 7.3), (53, 9.3), (57.6, 11.7), (61, 13.5), (63, 16.2)], )
        self.DrawLine([(52, 5), (57, 5.9), (63, 7), (69, 8), (71.8, 13.5), (61, 8.6)])
        self.DrawLine([(45, 2), (45, 5), (52, 5), (45, 2)])
        self.DrawLine(
            [(69, 8), (77.3, 0), (87.5, 4.7), (85.9, 6.8), (71.8, 13.5), (63, 16.2), (57, 18), (52.5, 18), (37, 14),
             (35, 9), (37, 3), (41, 3)])

        self.DrawLine([(63, 0), (63, 7), (57.6, 11.7), (52.5, 14), (52.5, 18)])
        self.DrawLine([(57, 0), (57, 5.9), (53, 9.3), (48.4, 11.5)])
        self.DrawLine([(52, 0), (52, 5), (49.4, 7.3), (45, 9.4)])
        self.DrawLine([(41, 3), (41, 7), (45, 9.4)])

        self.DrawLine([(45, 9.4), (48.4, 11.5), (52.5, 14)])
        self.DrawLine([(41.75, 1), (52.5, 5)])
        # self.DrawLine([(45.85, 2.75), (46.85, 3.0), (50.0, 4.0), (53.1, 5.0), (55.0, 5.8), (55.6, 6.0), (60.0, 6.8),(61.5, 7.0), (65.0, 7.35), (70.0, 7.85), (71.6, 8.0), (75.0, 8.3), (76.4, 8.4)])
        # self.DrawLine([(39.8, 0.35), (65.6, 9.7)])
        # self.DrawLine([(39.2, 0.0), (40.0, 0.4), (43.2, 2.0), (45.0, 2.8), (48.0, 4.0), (50.0, 4.75), (53.7, 6.0),(55.0, 6.4), (60.0, 8.0), (65.0, 8.8)])
        Labels = [u'F', u'Pc', u'U1', u'Ba', u'Bs', u'S1', u'U2', u'O1', u'S2', u'U3', u'O2', u'S3', u'Ph', u'O3', u'T',
                  u'Td', u'R', u'Q', u'S/N/L']
        Locations = [(39, 10), (43, 1.5), (44, 6), (47.5, 3.5), (49.5, 1.5), (49, 6), (49, 9.5), (54, 3), (53, 7),
                     (53, 12),
                     (60, 4),
                     (57, 8.5), (57, 14), (67, 5), (65, 12), (67, 9), (75, 9), (85, 1), (55, 18.5)]
        description = 'TAS (total alkali–silica) diagram (after Wilson et al. 1989).\nF Foidite, Ph Phonolite, Pc Pocrobasalt,\nU1 Tephrite (ol < 10%) Basanite(ol > 10%), U2 Phonotephrite, U3 Tephriphonolite,\nBa alkalic basalt,Bs subalkalic baslt, S1 Trachybasalt, S2 Basaltic Trachyandesite, S3 Trachyandesite,\nO1 Basaltic Andesite, O2 Andesite, O3 Dacite,  \nT Trachyte , Td Trachydacite , R Rhyolite, Q Silexite \n S/N/L Sodalitite/Nephelinolith/Leucitolith'
        tag = 'tas-Wilson1989-volcano'

        if (len(df) > 0):

            for i in range(len(df)):
                TmpLabel = ''
                if (df.at[i, 'Label'] in PointLabels or df.at[i, 'Label'] == ''):
                    TmpLabel = ''
                else:
                    PointLabels.append(df.at[i, 'Label'])
                    TmpLabel = df.at[i, 'Label']

                x.append(df.at[i, 'SiO2'])
                y.append(df.at[i, 'Na2O'] + df.at[i, 'K2O'])
                Size = df.at[i, 'Size']
                Color = df.at[i, 'Color']

                # print(Color, df.at[i, 'SiO2'], (df.at[i, 'Na2O'] + df.at[i, 'K2O']))

                Alpha = df.at[i, 'Alpha']
                Marker = df.at[i, 'Marker']
                Label = TmpLabel

                self.axes.scatter(df.at[i, 'SiO2'], (df.at[i, 'Na2O'] + df.at[i, 'K2O']), marker=df.at[i, 'Marker'],
                                  s=df.at[i, 'Size'], color=df.at[i, 'Color'], alpha=df.at[i, 'Alpha'], label=TmpLabel)

            # self.axes.savefig('tas.png', dpi=300, bbox_inches='tight')
            # self.axes.savefig('tas.svg', dpi=300, bbox_inches='tight')
            # self.axes.savefig('tas.pdf', dpi=300, bbox_inches='tight')
            # self.axes.savefig('tas.eps', dpi=300, bbox_inches='tight')
            # self.axes.show()

            self.draw()

    def TASv(self, df=pd.DataFrame(), Left=35, Right=79, X0=30, X1=90, X_Gap=7, Base=0,
             Top=19, Y0=1, Y1=19, Y_Gap=19, FontSize=12, xlabel=r'$SiO_2 wt\%$', ylabel=r'$na_2O + K_2O wt\%$',
             width=12, height=12, dpi=300, xlim=(30, 90), ylim=(0, 20)):

        PointLabels = []
        x = []
        y = []

        Labels = [u'F', u'Pc', u'U1', u'Ba', u'Bs', u'S1', u'U2', u'O1', u'S2', u'U3', u'O2', u'S3', u'Ph', u'O3', u'T',
                  u'Td', u'R', u'Q', u'S/N/L']
        Locations = [(39, 10), (43, 1.5), (44, 6), (47.5, 3.5), (49.5, 1.5), (49, 6), (49, 9.5), (54, 3), (53, 7),
                     (53, 12),
                     (60, 4),
                     (57, 8.5), (57, 14), (67, 5), (65, 12), (67, 9), (75, 9), (85, 1), (55, 18.5)]

        X_offset = -6
        Y_offset = 3

        TagNumber = min(len(Labels), len(Locations))

        for k in range(TagNumber):
            self.axes.annotate(Labels[k], Locations[k], xycoords='data', xytext=(X_offset, Y_offset),
                               textcoords='offset points',
                               fontsize=8, color='grey', alpha=0.8)

        self.DrawLine([(41, 0), (41, 3), (45, 3)])
        self.DrawLine([(45, 0), (45, 3), (45, 5), (49.4, 7.3), (53, 9.3), (57.6, 11.7), (61, 13.5), (63, 16.2)], )
        self.DrawLine([(52, 5), (57, 5.9), (63, 7), (69, 8), (71.8, 13.5), (61, 8.6)])
        self.DrawLine([(45, 2), (45, 5), (52, 5), (45, 2)])
        self.DrawLine(
            [(69, 8), (77.3, 0), (87.5, 4.7), (85.9, 6.8), (71.8, 13.5), (63, 16.2), (57, 18), (52.5, 18), (37, 14),
             (35, 9), (37, 3), (41, 3)])

        self.DrawLine([(63, 0), (63, 7), (57.6, 11.7), (52.5, 14), (52.5, 18)])
        self.DrawLine([(57, 0), (57, 5.9), (53, 9.3), (48.4, 11.5)])
        self.DrawLine([(52, 0), (52, 5), (49.4, 7.3), (45, 9.4)])
        self.DrawLine([(41, 3), (41, 7), (45, 9.4)])

        self.DrawLine([(45, 9.4), (48.4, 11.5), (52.5, 14)])
        # self.DrawLine([(41.75, 1), (52.5, 5)])
        # self.DrawLine([(45.85, 2.75), (46.85, 3.0), (50.0, 4.0), (53.1, 5.0), (55.0, 5.8), (55.6, 6.0), (60.0, 6.8),(61.5, 7.0), (65.0, 7.35), (70.0, 7.85), (71.6, 8.0), (75.0, 8.3), (76.4, 8.4)])
        # self.DrawLine([(39.8, 0.35), (65.6, 9.7)])
        # self.DrawLine([(39.2, 0.0), (40.0, 0.4), (43.2, 2.0), (45.0, 2.8), (48.0, 4.0), (50.0, 4.75), (53.7, 6.0),(55.0, 6.4), (60.0, 8.0), (65.0, 8.8)])
        Labels = [u'F', u'Pc', u'U1', u'Ba', u'Bs', u'S1', u'U2', u'O1', u'S2', u'U3', u'O2', u'S3', u'Ph', u'O3', u'T',
                  u'Td', u'R', u'Q', u'S/N/L']
        Locations = [(39, 10), (43, 1.5), (44, 6), (47.5, 3.5), (49.5, 1.5), (49, 6), (49, 9.5), (54, 3), (53, 7),
                     (53, 12),
                     (60, 4),
                     (57, 8.5), (57, 14), (67, 5), (65, 12), (67, 9), (75, 9), (85, 1), (55, 18.5)]
        description = 'TAS (total alkali–silica) diagram (after Wilson et al. 1989).\nF Foidite, Ph Phonolite, Pc Pocrobasalt,\nU1 Tephrite (ol < 10%) Basanite(ol > 10%), U2 Phonotephrite, U3 Tephriphonolite,\nBa alkalic basalt,Bs subalkalic baslt, S1 Trachybasalt, S2 Basaltic Trachyandesite, S3 Trachyandesite,\nO1 Basaltic Andesite, O2 Andesite, O3 Dacite,  \nT Trachyte , Td Trachydacite , R Rhyolite, Q Silexite \n S/N/L Sodalitite/Nephelinolith/Leucitolith'
        tag = 'tas-Wilson1989-volcano'

        if (len(df) > 0):

            for i in range(len(df)):
                TmpLabel = ''
                if (df.at[i, 'Label'] in PointLabels or df.at[i, 'Label'] == ''):
                    TmpLabel = ''
                else:
                    PointLabels.append(df.at[i, 'Label'])
                    TmpLabel = df.at[i, 'Label']

                x.append(df.at[i, 'SiO2'])
                y.append(df.at[i, 'Na2O'] + df.at[i, 'K2O'])
                Size = df.at[i, 'Size']
                Color = df.at[i, 'Color']

                # print(Color, df.at[i, 'SiO2'], (df.at[i, 'Na2O'] + df.at[i, 'K2O']))

                Alpha = df.at[i, 'Alpha']
                Marker = df.at[i, 'Marker']
                Label = TmpLabel

                self.axes.scatter(df.at[i, 'SiO2'], (df.at[i, 'Na2O'] + df.at[i, 'K2O']), marker=df.at[i, 'Marker'],
                                  s=df.at[i, 'Size'], color=df.at[i, 'Color'], alpha=df.at[i, 'Alpha'], label=TmpLabel,
                                  edgecolors='black')

            xLabel = r'$SiO_2 wt\%$' + '\n' + description
            yLabel = r'$na_2O + K_2O wt\%$'
            # self.axes.xlabel(xLabel, fontsize=12)

            self.draw()


class Lsq():
    xlist = [2.069, 5.862, 7.281, 3.336, 0.0723, 3.908, 0.1367, 11.29, 7.384, 2.861, 4.396, 9.231, 0.8056]
    ylist = [0.716972, 0.724464, 0.727566, 0.719333, 0.712823, 0.720578, 0.712962, 0.735598, 0.727391, 0.718462,
             0.721609, 0.731475, 0.714279]

    Xi = np.array(xlist)
    Yi = np.array(ylist)

    def __init__(self, parent=None, df=pd.DataFrame()):
        # TEST
        p0 = [100, 2]
        print(self.error(p0, self.Xi, self.Yi))

        ###主函数从此开始###
        s = "Test the number of iteration"  # 试验最小二乘法函数leastsq得调用几次error函数才能找到使得均方误差之和最小的k、b
        Para = leastsq(self.error, p0, args=(self.Xi, self.Yi, s))  # 把error函数中除了p以外的参数打包到args中
        k, b = Para[0]

    ###需要拟合的函数func及误差error###
    def func(self,p, x):
        k, b = p
        return k * x + b

    def error(self, p, x, y, s='error function'):
        print(s)
        return (self.func(p, x) - y)  # x、y都是列表，故返回值也是个列表




LocationOfMySelf=os.path.dirname(__file__)

#print(LocationOfMySelf,'Custom Bass Classes')