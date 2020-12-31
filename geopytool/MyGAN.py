from ImportDependence import *
from CustomClass import *


class MyGAN(AppForm):
    Lines = []
    Tags = []
    WholeData = []
    settings_backup=pd.DataFrame()
    description = 'Generative Adversarial Nets'
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


    n=6

    def __init__(self, parent=None, df=pd.DataFrame()):
        QMainWindow.__init__(self, parent)
        self._df = df
        self._df_back = df
        self.FileName_Hint = 'Generative Adversarial Nets'


        self.result_to_fit= self.Slim(self._df)
        self.low=0
        self.high=1

        for i in range(len(self.result_to_fit.values)):
            tmp_min=min(self.result_to_fit.values[i])
            tmp_max=max(self.result_to_fit.values[i])
            tmp_mean=np.mean(self.result_to_fit.values[i])
            tmp_std=np.std(self.result_to_fit.values[i])
            if tmp_min<self.low:
                self.low=tmp_min
            if tmp_max>self.high:
                self.high=tmp_max

        print('\nself.low ',self.low,'\nself.high ', self.high)

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


        self.feature_size=len(self.result_to_fit.values.T)
        self.original_size= len(self._df)
        self.target_size = self.original_size
        
        self.epochs_number = self.feature_size
        self.batch_size = int(self.original_size/self.feature_size)

        le = LabelEncoder()
        le.fit(self.result_to_fit.index)
        self.original_label = le.transform(self.result_to_fit.index)

        self.all_labels=[]
        self.all_colors=[]
        self.all_markers=[]
        self.all_alpha=[]
        self.color_list=[]
        self.data_indexed_dict={}

        for i in range(len(self._df)):
            target = self._df.at[i, 'Label']
            color = self._df.at[i, 'Color']
            marker = self._df.at[i, 'Marker']
            alpha = self._df.at[i, 'Alpha']

            if target not in self.all_labels:
                self.all_labels.append(target)
                self.all_colors.append(color)
                self.all_markers.append(marker)
                self.all_alpha.append(alpha)
            if color not in self.color_list:
                self.color_list.append(color)

        for k in self.all_labels:
            tmp_list=[]
            for i in range(len(self.Slim(self._df))):
                if self._df.at[i, 'Label'] == k:
                    tmp_list.append(self.result_to_fit.values[i])
            self.data_indexed_dict[k]=tmp_list
        self.columns_list = self.result_to_fit.columns.tolist()
        print('\nself.columns_list ',self.columns_list)
        self.create_main_frame()

    def create_main_frame(self):

        self.resize(800, 600)
        self.main_frame = QWidget()
        self.dpi = 128

        self.setWindowTitle('Generative Adversarial Nets')

        self.tableView = CustomQTableView(self.main_frame)
        self.tableView.setObjectName('tableView')
        self.tableView.setSortingEnabled(True)

        # Other GUI controls

        self.save_result_button = QPushButton('&Save GAN Result')
        self.save_result_button.clicked.connect(self.saveDataFile)

        self.run_gan_button = QPushButton('&Run GAN Again')
        self.run_gan_button.clicked.connect(self.Key_Func)

        self.sample_label = QLabel('Sample Size ')
        self.sample_seter = QLineEdit(self)
        self.sample_seter.textChanged[str].connect(self.Set_Target_Size)


        self.epochs_label = QLabel('Epochs Number ')
        self.epochs_seter = QLineEdit(self)
        self.epochs_seter.textChanged[str].connect(self.Set_Epochs_Number)


        self.batch_label = QLabel('Batch Size ')
        self.batch_seter = QLineEdit(self)
        self.batch_seter.textChanged[str].connect(self.Set_Batch_Size)


        self.vbox = QVBoxLayout()
        self.hbox = QHBoxLayout()


        self.vbox.addWidget(self.tableView)


        for w in [self.sample_label, self.sample_seter, self.epochs_label, self.epochs_seter, self.batch_label,self.batch_seter,self.save_result_button, self.run_gan_button]:
            self.hbox.addWidget(w)
            self.hbox.setAlignment(w, Qt.AlignVCenter)

        self.vbox.addLayout(self.hbox)
        self.main_frame.setLayout(self.vbox)
        self.setCentralWidget(self.main_frame)




    def Key_Func(self):
        df_list=[]


        print('feature_size ',self.feature_size,'\noriginal_size ',
              self.original_size,'\ntarget_size ',self.target_size,'\nepochs_number ',self.epochs_number)

        for k in self.all_labels:
            tmp_list=[]
            for i in range(len(self.Slim(self._df))):
                if self._df.at[i, 'Label'] == k:
                    # tmp_list.append(self._df.loc[i])
                    tmp_list.append(self.result_to_fit.values[i])
                self.data_indexed_dict[k] = tmp_list
            self.data_indexed_dict[k]=tmp_list

            tmp_data=pd.DataFrame(tmp_list)
            tmp_result = self.training(epochs = self.epochs_number, batch_size = self.batch_size, data=tmp_data)
            tmp_label = (k,)*len(tmp_result)
            tmp_combine = pd.concat(
                [pd.DataFrame(tmp_label), pd.DataFrame(tmp_result)],
                axis=1)
            tmp_combine.columns=['Label']+self.columns_list
            df_list.append(tmp_combine)

        self.whole_labels = self.all_labels

        self.result = pd.concat(df_list, sort=False, axis=0)
        self.model = PandasModel(self.result)
        self.tableView.setModel(self.model)

    def Set_Target_Size(self,text):
        try:
            self.target_size= int(text)
            # if self.target_size < self.original_size:
            #     self.target_size = self.original_size
                #self.ErrorEvent(text=repr('Target size must be larger than original.'))
        except:
            pass
    def Set_Epochs_Number(self,text):
        try:
            self.epochs_number= int(text)
            # if self.epochs_number < self.feature_size:
            #     self.epochs_number = self.feature_size
                #self.ErrorEvent(text=repr('Epochs must be larger than 1.'))
        except:
            pass

    def Set_Batch_Size(self,text):
        try:
            self.batch_size= int(text)
            # if self.batch_size < int(self.original_size/self.feature_size):
            #     self.batch_size = int(self.original_size/self.feature_size)
                #self.ErrorEvent(text=repr('Batch_S ize must be larger than 10 .'))
        except:
            pass


    def adam_optimizer(self,): # 定义优化器
        return Adam(lr=0.0002, beta_1=0.5)

    def create_generator(self,): # 定义生成器
        generator = Sequential()
        generator.add(Dense(units=256, input_dim = self.feature_size))
        generator.add(LeakyReLU(0.2))

        generator.add(Dense(units=512))
        generator.add(LeakyReLU(0.2))

        generator.add(Dense(units=1024))
        generator.add(LeakyReLU(0.2))

        generator.add(Dense(units = self.feature_size, activation='tanh'))

        generator.compile(loss='binary_crossentropy', optimizer=self.adam_optimizer())
        return generator

    def create_discriminator(self,): # 定义判别器
        discriminator = Sequential()
        discriminator.add(Dense(units=1024, input_dim=self.feature_size))
        discriminator.add(LeakyReLU(0.2))
        discriminator.add(Dropout(0.3))

        discriminator.add(Dense(units=512))
        discriminator.add(LeakyReLU(0.2))
        discriminator.add(Dropout(0.3))

        discriminator.add(Dense(units=256))
        discriminator.add(LeakyReLU(0.2))

        discriminator.add(Dense(units=1, activation='sigmoid'))

        discriminator.compile(loss='binary_crossentropy', optimizer=self.adam_optimizer())
        return discriminator

    def create_gan(self,discriminator, generator):
        discriminator.trainable=False
        # 这是一个链式模型：输入经过生成器、判别器得到输出
        gan_input = Input(shape=(self.feature_size,))
        x = generator(gan_input)
        gan_output= discriminator(x)
        gan= Model(inputs=gan_input, outputs=gan_output)
        gan.compile(loss='binary_crossentropy', optimizer='adam')
        return gan

    def training(self,epochs = 1,batch_size = 3,data=pd.DataFrame([1,2,3,4])):
        batch_count = len(data)/ batch_size
        generator = self.create_generator()
        discriminator = self.create_discriminator()
        gan = self.create_gan(discriminator, generator)

        for e in range(1, epochs + 1):
            # print("Epoch %d" % e)
            for _ in tqdm(range(int(batch_count))):
                # 产生噪声喂给生成器
                # noise = np.random.normal(self.low, self.high, [batch_size, self.feature_size])

                noise = np.random.normal((self.low+self.high)/2, (self.high-self.low)/2, [batch_size, self.feature_size])

                # clf = mixture.BayesianGaussianMixture(n_components=self.feature_size, covariance_type='full')

                # 产生假数据
                generated_data = generator.predict(noise)

                print(len(noise))
                print('\nnoise.shape ',noise.shape)

                # 一组随机真数据
                tmp_index= np.random.randint(low=0, high=(len(data)-1), size=batch_size)
                print('\ntmp_index ',tmp_index)

                data_batch =np.array(data)[tmp_index]

                # data_batch = data[np.random.randint(low=0, high=(len(data)-1), size=batch_size)]

                print('\ndata_batch ',data_batch.shape,'\ngenerated_data',generated_data.shape)


                # 真假数据拼接
                X = np.concatenate([data_batch, generated_data])

                # 生成数据和真实数据的标签
                y_dis = np.zeros(2 * batch_size)
                y_dis[:batch_size] = 0.9

                # 预训练，判别器区分真假
                discriminator.trainable = True
                discriminator.train_on_batch(X, y_dis)

                # 欺骗判别器 生成的数据为真的数据
                # noise = np.random.normal(self.low, self.high, [batch_size, self.feature_size])
                noise = np.random.normal((self.low+self.high)/2, (self.high-self.low)/2, [batch_size, self.feature_size])

                y_gen = np.ones(batch_size)

                # GAN的训练过程中判别器的权重需要固定
                discriminator.trainable = False

                # GAN的训练过程为交替“训练判别器”和“固定判别器权重训练链式模型”
                gan.train_on_batch(noise, y_gen)

            # if e == 1 or e % 50 == 0:
            #     看一下生成器能生成什么
        # noise = np.random.normal(self.low, self.high, [self.target_size, self.feature_size])

        noise = np.random.normal(0,1, [self.target_size, self.feature_size])

        result = generator.predict(noise)
        return result





