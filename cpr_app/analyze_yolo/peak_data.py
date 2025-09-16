class PeakData:
    def __init__(self):
        #名前かぶりを避けるために頭に_を入れている
        #ピークのインデックスの配列
        #peak_upper_indexesとpeak_lower_indexesと書かれている場合あり
        self._recoil_order_list = []
        self._depth_order_list = []
        #実際の値の配列
        #peak_upper_valuesとpeak_lower_valuesと書かれている場合あり
        self._recoil_values = []
        self._depth_values = []
        #peak_upper_countとpeak_lower_countと書かれている場合あり
        self._peak_recoil_count = 0
        self._peak_depth_count = 0
    
    #pd_appro用
    def setup(self,pd):
        self._recoil_order_list = pd.recoil_order_list[:]
        self._depth_order_list = pd.depth_order_list[:]
        self._recoil_values = pd.recoil_values[:]
        self._depth_values = pd.depth_values[:]
        self._peak_recoil_count = pd.peak_recoil_count
        self._peak_depth_count = pd.peak_depth_count

    def setup_values(self,depth_values,recoil_values):
        self._depth_values = depth_values
        self._recoil_values = recoil_values
    
    def setup_peak_count(self,peak_depth_count, peak_recoil_count):
        self._peak_recoil_count = peak_recoil_count
        self._peak_depth_count = peak_depth_count
    
    def setup_order_list(self,depth_order_list,recoil_order_list):
        self._depth_order_list =depth_order_list
        self._recoil_order_list = recoil_order_list

    @property
    def recoil_order_list(self):
        return self._recoil_order_list

    @recoil_order_list.setter
    def recoil_order_list(self, List):
        List.sort()
        self._recoil_order_list = List

    @property
    def depth_order_list(self):
        return self._depth_order_list

    @depth_order_list.setter
    def depth_order_list(self, List):
        List.sort()
        self._depth_order_list = List

    @property
    def recoil_values(self):
        return self._recoil_values

    @recoil_values.setter
    def recoil_values(self, List):
        List.sort()
        self._recoil_values = List

    @property
    def depth_values(self):
        return self._depth_values

    @depth_values.setter
    def depth_values(self, List):
        List.sort()
        self._depth_values = List
    
    @property
    def peak_recoil_count(self):
        return self._peak_recoil_count
    
    @property
    def peak_depth_count(self):
        return self._peak_depth_count
    
    def print_contents(self):
        print("recoil_order_list ", self._recoil_order_list)
        print("depth_order_list " ,self._depth_order_list)
        print("recoil_values ", self._recoil_values)
        print("depth_values ",self._depth_values)
        print("peak_recoil_count ", self._peak_recoil_count)
        print("peak_depth_count ",self._peak_depth_count)

class PeakDataAppropriate(PeakData):
    def __init__(self,pd = None):
        self._appro_recoils_indexes = []
        self._appro_compression_indexes = []
        self._appro_recoils_percent = 0
        self._appro_compression_percent =0
        super().__init__()
        if pd is not None:
            self.setup(pd=pd)
    
    def setup_appro(self,appro_recoils_indexes,appro_compression_indexes,appro_recoils_percent,appro_compression_percent):
        self._appro_recoils_indexes = appro_recoils_indexes
        self._appro_compression_indexes = appro_compression_indexes
        self._appro_recoils_percent = appro_recoils_percent
        self._appro_compression_percent = appro_compression_percent

    @property
    def appro_recoils_indexes(self):
        return self._appro_recoils_indexes
    
    @property
    def appro_compression_indexes(self):
        return self._appro_compression_indexes

    @property
    def appro_recoils_percent(self):
        return self._appro_recoils_percent

    @property
    def appro_compression_percent(self):
        return self._appro_compression_percent

    def print_contents(self):
        super().print_contents()
        print("Appro Recoils Indexes:", self._appro_recoils_indexes)
        print("Appro Compression Indexes:", self._appro_compression_indexes)
        print("Appro Recoils Percent:", self._appro_recoils_percent)
        print("Appro Compression Percent:", self._appro_compression_percent)

# #ここでやりたいことはpeak_data_outputで
# class PeakDataOutput(PeakDataAppropriate):
#     #output用のデータを保存するclass
#     #わかりにくいからちょっと整えてもいいかも
#     def __init__(self,pd = None):
        
#         if pd is not None:
#             super().__init__(pd)
#         else:
#             super().__init__()

#     @property
#     def evaluation_outputs(self):
#         return self._evaluation_outputs
    
#     def set_output(self,pd,compression_count,mean_tempo,appro_tempo_percent):
#         self._evaluation_outputs["compression_count"] = compression_count
#         self._evaluation_outputs["appro_recoils_percent"]= pd.appro_recoils_percent
#         self._evaluation_outputs["appro_compression_percent"] = pd.appro_compression_percent,
#         self._evaluation_outputs["mean_tempo"] = mean_tempo
#         self._evaluation_outputs["appro_tempo_percent"] = appro_tempo_percent
    
#     def add_output(self,index_text,data):
#         self._evaluation_outputs[index_text] = data

#     def swap_output(self,data):
#         self._evaluation_outputs = {}
#         self._evaluation_outputs = data







