# coding=utf-8
from nlpir.native.nlpir_base import NLPIRBase
from ctypes import c_bool, c_char, c_char_p, c_double, c_int, c_uint, POINTER, Structure, byref, c_float
import typing


class StDoc(Structure):
    __fields__ = [
        ("sTitle", c_char_p),
        ("sContent", c_char_p),
        ("sAuthor", c_char_p),
        ("sBoard", c_char_p),
        ("sDatatype", c_char_p)
    ]


class Classifier(NLPIRBase):
    @property
    def dll_name(self):
        return "LJClassifier"

    @NLPIRBase.byte_str_transform
    def init_lib(self, data_path: str, encode: int, license_code: str) -> int:
        """
            // 功能：  文件方式初始化
            // 返回值：成功/失败
            // 出错信息记录在硬盘的./ljclassifier.log和./DataFile/ljclassifier.log上
        :param data_path:
        :param encode:
        :param license_code:
        :return:
        """
        return self.get_func("classifier_init", [c_char_p, c_char_p, c_char_p], c_bool)("rulelist.xml", data_path,
                                                                                        license_code)

    @NLPIRBase.byte_str_transform
    def exit_lib(self) -> bool:
        """

        :return:
        """
        return self.get_func("classifier_exit", None, None)()

    @NLPIRBase.byte_str_transform
    def get_last_error_msg(self) -> str:
        return self.get_func("classifier_GetLastErrorMsg", None, c_char_p)()

    @NLPIRBase.byte_str_transform
    def exec_1(self, data: StDoc, out_type: int = 0):
        """
        // 功能：对输入的文章结构进行分类
        // 参数：d:文章结构指针
        //       iType=0:  输出类名，各类之间用\t隔开  内容格式举例：“要闻	敏感	诉讼”
        //       iType=1:  输出类名和置信度，各类之间用\t隔开，类名和权重用“ ”隔开   内容格式举例：“要闻 1.00	敏感 0.95	诉讼 0.82”
        //       iType 默认值为0
        // 返回值：主题类别串  各类之间用\t隔开，类名按照置信度从高到低排序
        :param data:
        :param type:
        :return:
        """
        return self.get_func("classifier_exec1", [POINTER(StDoc), c_int], c_char_p)(data, out_type)

    @NLPIRBase.byte_str_transform
    def exec(self, title: str, content: str, out_type: int):
        """
        // 功能：对输入的文章结构进行分类
        // 参数：d:文章结构指针
        //       iType=0:  输出类名，各类之间用\t隔开  内容格式举例：“要闻	敏感	诉讼”
        //       iType=1:  输出类名和置信度，各类之间用\t隔开，类名和权重用“ ”隔开   内容格式举例：“要闻 1.00	敏感 0.95	诉讼 0.82”
        //       iType 默认值为0
        // 返回值：主题类别串  各类之间用\t隔开，类名按照置信度从高到低排序
        :param title:
        :param content:
        :param out_type:
        :return:
        """
        return self.get_func("classifier_exec")([c_char_p, c_char_p, c_int], c_char_p)(title, content, out_type)

    @NLPIRBase.byte_str_transform
    def detail(self, classname: str):
        """

        // 功能：对于当前文档，输入类名，取得结果明细
        // 参数：classname:结果类名
        // 返回值：结果明细 例如:
        /*		   RULE3:
        SUBRULE1: 内幕 1
        SUBRULE2: 股市 1	基金 3	股票 8
        SUBRULE3: 书摘 2	*/
        :param classname:
        :return:
        """
        return self.get_func("classifier_detail", [c_char_p], c_char_p)(classname)

    @NLPIRBase.byte_str_transform
    def set_sim_thresh(self, sim: float):
        """

        :param sim:
        :return:
        """
        return self.get_func("classifier_setsimthresh", [c_float])(sim)
