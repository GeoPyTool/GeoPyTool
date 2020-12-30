from ImportDependence import *
from CustomClass import *


class MyMLP(AppForm):
    Lines = []
    Tags = []
    WholeData = []
    settings_backup=pd.DataFrame()
    description = 'Multilayer Perceptron'
    unuseful = ['Name', 
                'Mineral', 
                'Author', 
                'DataType', 
                'Label', 
                'Marker', 
                'Color', 
                'Size', 
                'Alpha', 
                'Style', 
                'Width', 
                'Tag']
    data_to_test=pd.DataFrame()
    text_result = ''
    whole_labels=[]



    MLP=MLPClassifier()
    n=6

    def __init__(self, parent=None, df=pd.DataFrame()):
        QMainWindow.__init__(self, parent)
        self._df = df
        self._df_back = df
        self.FileName_Hint = 'Multilayer Perceptron'

        if (len(df) > 0):
            self._changed = True
            # print('DataFrame recieved to Neural Network')

        self.settings_backup = self._df
        ItemsToTest = ['Label', 'Number', 'Tag', 'Name', 'Author', 'DataType', 'Marker', 'Color', 'Size', 'Alpha', 
                       'Style', 'Width']
        for i in self._df.columns.values.tolist():
            if i not in ItemsToTest:
                self.settings_backup = self.settings_backup.drop(i, 1)
        #print(self.settings_backup)


        self.result_to_fit= self.Slim(self._df)

        # There is an article that proposes a method to find out how many neurons should be in a hidden layer. According to Sheela and Deepa (2013) number of neurons
        # can be calculated in a hidden layer as (4*n^2+3)/(n^2-8) where n is the number of input.
        # On the other hand, number of hidden layer can be 2 in little data set. (0,10) in the large data set that can be adjusted according to the accuracy of MSE etc.
        # The study is Sheela, K. G., & Deepa, S. N. (2013). Review on methods to fix number of hidden neurons in neural networks. Mathematical Problems in Engineering, 2013.
        # https://www.researchgate.net/post/How-to-choose-size-of-hidden-layer-and-number-of-layers-in-an-encoder-decoder-RNN
        # self.MLP = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(3,3), random_state=1)

        #(4 * n ^ 2 + 3) / (n ^ 2 - 8)
        # 注意：默认solver ‘adam’在相对较大的数据集上效果比较好（几千个样本或者更多）
        # 对小数据集来说，lbfgs 收敛更快效果也更好。

        n = len(self.result_to_fit)

        # n 是原始训练集的样本数
        # 用原始训练集中样本的维度作为输入层神经元个数
        # 用原始训练集中样本的类别标签数作为输出层神经元个数
        # m 是根据上面参考文献得到的经验公式，作为隐藏神经元层数

        m = int((4 * n**2 + 3)/(n** 2 - 8))
        print('self.result_to_fit is \n',self.result_to_fit,'\n')
        input_size = len(self.result_to_fit.values.T)
        output_size = len(set(self.result_to_fit.index))
        alpha= 2 # 2-10

        # if (2<=m<=10):
        #     alpha = m  # 2-10
        # else:
        #     alpha = 5
        # n_h 是得到的隐藏层的每一层神经元个数
        n_h= int(n/(alpha*(input_size+output_size)))

        print('input_size=',input_size,'\noutput_size=',output_size,'\nn_h=',n_h,'\nm=',m)

        self.input_size = input_size # 输入层神经元个数
        self.output_size = output_size # 输出层神经元个数
        self.n = n  # n 是原始训练集的样本数
        self.m = m  # m 是根据上面参考文献得到的经验公式，作为隐藏神经元层数
        self.n_h = n_h # n_h 是得到的隐藏层的每一层神经元个数

        le = LabelEncoder()
        le.fit(self.result_to_fit.index)
        self.original_label = le.transform(self.result_to_fit.index)


        self.create_main_frame()

    def create_main_frame(self):

        self.resize(800, 600)
        self.main_frame = QWidget()
        self.dpi = 128
        self.fig = Figure((8.0, 6.0), dpi=self.dpi)

        self.setWindowTitle('Multilayer Perceptron Classification')

        #self.fig.subplots_adjust(hspace=0.5, wspace=0.5, left=0.3, bottom=0.3, right=0.7, top=0.9)
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self.main_frame)

        # self.layer_seter = QLineEdit(self)
        # self.layer_seter.textChanged[str].connect(self.Key_Func)

        # self.legend_cb = QCheckBox('&Legend')
        # self.legend_cb.setChecked(True)
        # self.legend_cb.stateChanged.connect(self.Key_Func)  # int

        # self.show_load_data_cb = QCheckBox('&Show Loaded Data')
        # self.show_load_data_cb.setChecked(True)
        # self.show_load_data_cb.stateChanged.connect(self.Key_Func)  # int

        # self.show_data_index_cb = QCheckBox('&Show Data Index')
        # self.show_data_index_cb.setChecked(False)
        # self.show_data_index_cb.stateChanged.connect(self.Key_Func)  # int

        # self.shape_cb= QCheckBox('&Shape')
        # self.shape_cb.setChecked(False)
        # self.shape_cb.stateChanged.connect(self.Key_Func)  # int

        # self.hyperplane_cb= QCheckBox('&Hyperplane')
        # self.hyperplane_cb.setChecked(False)
        # self.hyperplane_cb.stateChanged.connect(self.Key_Func)  # int

        self.mpl_toolbar = NavigationToolbar(self.canvas, self.main_frame)

        # Other GUI controls
        self.save_picture_button = QPushButton('&Save Picture')
        self.save_picture_button.clicked.connect(self.saveImgFile)

        # self.save_result_button = QPushButton('&Show MLP Result')
        # self.save_result_button.clicked.connect(self.showResult)

        self.save_Para_button = QPushButton('&Show MLP Para')
        self.save_Para_button.clicked.connect(self.showPara)

        self.save_predict_button = QPushButton('&Show Predict Result')
        self.save_predict_button.clicked.connect(self.showPredictResult)

        self.load_data_button = QPushButton('&Add Data to Test')
        self.load_data_button.clicked.connect(self.loadDataToTest)

        # self.slider_left_label = QLabel('Same Size Neurons')
        # self.slider_right_label = QLabel('Asymptotic Neurons')
        # self.slider = QSlider(Qt.Horizontal)
        # self.slider.setRange(0, 1)
        # self.slider.setValue(0)
        # self.slider.setTracking(True)
        # self.slider.setTickPosition(QSlider.TicksBothSides)
        # self.slider.valueChanged.connect(self.Key_Func)  # int

        # self.kernel_select = QSlider(Qt.Horizontal)
        # self.kernel_select.setRange(0, len(self.kernel_list)-1)
        # self.kernel_select.setValue(0)
        # self.kernel_select.setTracking(True)
        # self.kernel_select.setTickPosition(QSlider.TicksBothSides)
        # self.kernel_select.valueChanged.connect(self.Key_Func)  # int
        # self.kernel_select_label = QLabel('Kernel')

        self.vbox = QVBoxLayout()
        self.hbox = QHBoxLayout()
        self.hbox0 = QHBoxLayout()
        self.hbox1 = QHBoxLayout()
        self.hbox2 = QHBoxLayout()
        self.hbox3 = QHBoxLayout()
        self.hbox4 = QHBoxLayout()

        self.vbox.addWidget(self.mpl_toolbar)
        self.vbox.addWidget(self.canvas)

        # for w in [self.legend_cb, self.show_load_data_cb, self.show_data_index_cb, self.shape_cb, self.hyperplane_cb,self.kernel_select_label,self.kernel_select ]:
        #     self.hbox0.addWidget(w)
        #     self.hbox0.setAlignment(w, Qt.AlignVCenter)

        # for w in [self.slider_left_label,self.slider,self.slider_right_label ]:
        #     self.hbox0.addWidget(w)
        #     self.hbox0.setAlignment(w, Qt.AlignVCenter)

        for w in [self.load_data_button, self.save_picture_button, self.save_Para_button, self.save_predict_button]:
            self.hbox1.addWidget(w)
            self.hbox1.setAlignment(w, Qt.AlignVCenter)

        self.vbox.addLayout(self.hbox0)
        self.vbox.addLayout(self.hbox1)

        self.axes = self.fig.add_subplot(111)


        self.main_frame.setLayout(self.vbox)
        self.setCentralWidget(self.main_frame)
        #self.show()



    def Key_Func(self):

        self.axes.clear()
        #print(self.result_to_fit.columns.values.tolist())
        #MLP Fitting
        hidden_layer_tuple=(self.n_h,) * self.m

        self.MLP = MLPClassifier(solver='lbfgs', alpha=1e-5,
                                 hidden_layer_sizes=hidden_layer_tuple,
                                 random_state=1)

        try:
            self.MLP.fit(self.result_to_fit.values, self.result_to_fit.index)
            self.coefs_ = self.MLP.coefs_
            self.intercepts_ = self.MLP.intercepts_
            self.MLP_params= self.MLP.get_params(deep = True)
            self.Para = pd.DataFrame(self.MLP_params)

            self.input_size    # 输入层神经元个数
            self.output_size   # 输出层神经元个数
            self.n  # n 是原始训练集的样本数
            self.m # m 是根据上面参考文献得到的经验公式，作为隐藏神经元层数
            self.n_h  # n_h 是得到的隐藏层的每一层神经元个数


            # 接下来需要做的就是训练参数的保存、加载
            # 或许可以推广到其他类型模型的参数保存和加载

            center=(0,0)
            circ_input=[]

            input_layer=[]
            middle_layers=[]
            output_layer=[]

            # 绘制输入层神经元
            for i in range(self.input_size):
                # 旧方法用的是画圆然后一个个放上去，新方法改成了scatter投点了，不需要了
                # circ_tmp = plt.Circle((0, i), 0.3, fc='blue', alpha=0.3)
                # circ_input.append(circ_tmp)
                # self.axes.add_patch(circ_tmp)
                input_layer.append([0,i])
                self.axes.scatter(0, i,
                                  marker= 'o',
                                  s=5, color='blue',
                                  alpha=0.3,
                                  label='Input Layer')

            # 绘制隐藏层神经元
            for i in range(self.m):
                middle_tmp_layer=[]
                for j in range(self.n_h):
                    middle_tmp_layer.append([i+2, self.input_size/2-self.n_h/2+j])
                    self.axes.scatter(i+2, self.input_size/2-self.n_h/2+j,
                                      marker='o',
                                      s=5,
                                      color='grey',
                                      alpha=0.3,
                                      label='Output Layer')
                middle_layers.append(middle_tmp_layer)

            # 绘制输出层神经元
            for i in range(self.output_size):
                # 旧方法用的是画圆然后一个个放上去，新方法改成了scatter投点了，不需要了
                # circ_tmp = plt.Circle((self.m+3, self.input_size/2+i), 0.3, fc='red', alpha=0.3)
                # circ_input.append(circ_tmp)
                # self.axes.add_patch(circ_tmp)
                output_layer.append([self.m+3, self.input_size/2-self.output_size/2+i])
                self.axes.scatter(self.m+3, self.input_size/2-self.output_size/2+i,
                                  marker='o',
                                  s=5,
                                  color='red',
                                  alpha=0.3,
                                  label='Output Layer')

            for i in input_layer:
                for j in middle_layers[0]:
                    self.axes.plot([i[0], j[0]],[i[1],j[1]],color= 'grey', linewidth=1,
                               linestyle='-', alpha=1/self.input_size)

            for i in output_layer:
                for j in middle_layers[-1]:
                    self.axes.plot([i[0], j[0]],[i[1],j[1]] ,color= 'grey', linewidth=1,
                               linestyle='-', alpha=1/self.output_size)

            for i in range(len(middle_layers)):
                if i >0:
                    for j in middle_layers[i]:
                        for k in middle_layers[i-1]:
                            self.axes.plot([k[0], j[0]],[k[1],j[1]], color='grey', linewidth=0.5,
                                       linestyle='-', alpha=1/self.n_h)

            # self.axes.set_xlim([-1, self.m+4])
            # self.axes.set_ylim([-1,self.input_size+2])

            self.axes.get_xaxis().set_visible(False)
            self.axes.get_yaxis().set_visible(False)
            # 设置横纵单元为相等，保证圆形的比例，改成scatter后就不用了
            # self.axes.set_aspect('equal')


        except Exception as e:
            self.ErrorEvent(text=repr(e))


        all_labels=[]
        all_colors=[]
        all_markers=[]
        all_alpha=[]

        self.color_list=[]

        for i in range(len(self._df)):
            target = self._df.at[i, 'Label']
            color = self._df.at[i, 'Color']
            marker = self._df.at[i, 'Marker']
            alpha = self._df.at[i, 'Alpha']

            if target not in all_labels:
                all_labels.append(target)
                all_colors.append(color)
                all_markers.append(marker)
                all_alpha.append(alpha)
            if color not in self.color_list:
                self.color_list.append(color)

        self.whole_labels = all_labels

        if(len(self.data_to_test)>0):

            contained = True
            missing = 'Miss setting infor:'

            for i in ['Label', 'Color', 'Marker', 'Alpha']:
                if i not in self.data_to_test.columns.values.tolist():
                    contained = False
                    missing = missing +'\n' + i

            if contained == True:

                for i in self.data_to_test.columns.values.tolist():
                    if i not in self._df.columns.values.tolist():
                        self.data_to_test=self.data_to_test.drop(columns=i)

                #print(self.data_to_test)

                test_labels=[]
                test_colors=[]
                test_markers=[]
                test_alpha=[]


                for i in range(len(self.data_to_test)):
                    target = self.data_to_test.at[i, 'Label']
                    color = self.data_to_test.at[i, 'Color']
                    marker = self.data_to_test.at[i, 'Marker']
                    alpha = self.data_to_test.at[i, 'Alpha']

                    if target not in test_labels and target not in all_labels:
                        test_labels.append(target)
                        test_colors.append(color)
                        test_markers.append(marker)
                        test_alpha.append(alpha)


                self.whole_labels = self.whole_labels +test_labels

                self.data_to_test_to_fit= self.Slim(self.data_to_test)



                self.load_settings_backup = self.data_to_test
                Load_ItemsToTest = ['Label', 'Number', 'Tag', 'Name', 'Author', 'DataType', 'Marker', 'Color', 'Size', 
                               'Alpha', 'Style', 'Width']
                for i in self.data_to_test.columns.values.tolist():
                    if i not in Load_ItemsToTest:
                        self.load_settings_backup = self.load_settings_backup.drop(i, 1)


        self.result = pd.concat([self.begin_result , self.load_result], sort=False, axis=0)
        self.canvas.draw()

    def showPredictResult(self):

        # try:

        self.MLP.fit(self.result_to_fit.values , self.result_to_fit.index)
        self.coefs_ = self.MLP.coefs_
        self.intercepts_ = self.MLP.intercepts_
        self.MLP_params= self.MLP.get_params(deep = True)
        self.data_to_test = self.Slim(self.data_to_test)

        print('self.data_to_test is \n', self.data_to_test, '\n')

        Z = self.MLP.predict( self.data_to_test.values )

        Z2 = self.MLP.predict_proba( self.data_to_test.values )
        proba_df = pd.DataFrame(Z2)
        proba_df.columns = self.MLP.classes_

        proba_list = []
        for i in range(len(proba_df)):
            proba_list.append(round(max(proba_df.iloc[i])+ 0.001, 2))
        predict_result = pd.concat(
            [self.load_settings_backup['Label'], pd.DataFrame({'Classification': Z}), pd.DataFrame({'Confidence probability': proba_list})],
            axis=1)
        #print(predict_result)

        self.predictpop = TableViewer(df=predict_result,
                                      title=self.description + ' Predict Result')
        self.predictpop.show()

        # except Exception as e:
        #     msg = 'You need to load another data to run MLP.\n '
        #     self.ErrorEvent(text= msg +repr(e) )

    def Distance_Calculation(self):

        print(self.whole_labels)
        distance_result={}

        print(distance_result)

        for i in range(len(self.whole_labels)):
            print( self.whole_labels[i], len(self.MLP_result[self.result_to_fit.index == self.whole_labels[i]]))


