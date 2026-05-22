# -*- coding: utf-8 -*-
"""
Internationalization (i18n) Module

Provides multi-language support for the GUI interface.
"""

import json
import os
from typing import Dict, Optional

_current_lang = 'en'
_translations: Dict[str, Dict[str, str]] = {}

TRANSLATIONS = {
    'en': {
        # Menu
        'menu_file': '&File',
        'menu_geochemistry': '&Geochemistry',
        'menu_analysis': '&Analysis',
        'menu_isotopes': '&Isotopes',
        'menu_tools': '&Tools',
        'menu_help': '&Help',
        
        # File menu
        'action_open': '&Open...',
        'action_save': '&Save...',
        'action_quit': '&Quit',
        
        # Geochemistry menu
        'action_tas': 'TAS Diagram',
        'action_ree': 'REE Spider Diagram',
        'action_trace': 'Trace Element Diagram',
        'action_harker': 'Harker Diagram',
        'action_pearce': 'Pearce Tectonic Diagram',
        'menu_triangular': 'Triangular Diagrams',
        'action_qapf': 'QAPF Diagram',
        'action_qfl': 'QFL Diagram',
        
        # Analysis menu
        'action_pca': 'PCA',
        'action_cluster': 'Cluster Analysis',
        'action_statistics': 'Statistics',
        'menu_ml': 'Machine Learning',
        'action_svm': 'SVM Classification',
        'action_lda': 'LDA Analysis',
        'action_mlp': 'MLP Neural Network',
        'action_pca_ml': 'PCA Analysis',
        
        # Isotopes menu
        'action_rbsr': 'Rb-Sr Isochron',
        'action_smnd': 'Sm-Nd Isochron',
        'action_kar': 'K-Ar Isochron',
        'action_arar': 'Ar-Ar Isochron',
        
        # Tools menu
        'action_cipw': 'CIPW Norm Calculator',
        'action_combine': 'Combine Data',
        'action_flatten': 'Flatten Data',
        'action_zircon_ce': 'Zircon Ce Oxygen Fugacity',
        
        # Help menu
        'action_about': '&About',
        
        # Toolbar
        'toolbar_open': 'Open',
        'toolbar_save': 'Save',
        'toolbar_tas': 'TAS',
        'toolbar_ree': 'REE',
        'toolbar_trace': 'Trace',
        'toolbar_harker': 'Harker',
        
        # Status
        'status_ready': 'Ready',
        'status_loaded': 'Loaded',
        
        # Dialogs
        'dialog_open_file': 'Open Data File',
        'dialog_save_file': 'Save Data File',
        'dialog_save_image': 'Save Image',
        'dialog_save_cipw': 'Save CIPW Results',
        'dialog_save_zircon_ce': 'Save Zircon Ce Results',
        'dialog_save_figure': 'Save Figure',
        'filter_all': 'All Supported (*.csv *.xlsx *.xls)',
        'filter_csv': 'CSV Files (*.csv)',
        'filter_excel': 'Excel Files (*.xlsx *.xls)',
        'filter_png': 'PNG Files (*.png)',
        'filter_pdf': 'PDF Files (*.pdf)',
        'filter_svg': 'SVG Files (*.svg)',
        
        # Messages
        'msg_no_data': 'No data to save.',
        'msg_no_results': 'No results to save. Calculate first.',
        'msg_load_first': 'Please load data first.',
        'msg_save_success': 'Saved to',
        'msg_calc_success': 'Calculated CIPW norms for {} samples.',
        'msg_no_calc': 'Calculate CIPW first.',
        'msg_zircon_ce_no_result': 'No valid Zircon Ce results. Check data.',
        'msg_zircon_ce_calc_success': 'Calculated Zircon Ce4+/Ce3+ for {} samples.',
        'msg_file_saved': 'File saved successfully.',
        'msg_error': 'Error',
        'msg_warning': 'Warning',
        'msg_success': 'Success',
        
        # Labels
        'label_rows': 'Rows:',
        'label_columns': 'Columns:',
        'label_x_axis': 'X-axis:',
        'label_y_axis': 'Y-axis:',
        'label_diagram': 'Diagram:',
        'label_kernel': 'Kernel:',
        'label_linkage': 'Linkage:',
        'label_distance': 'Distance:',
        'label_clusters': 'Clusters:',
        'label_type': 'Type:',
        'label_columns_count': 'Columns:',
        'label_component': 'component',
        'label_results': 'Results:',
        
        # Buttons
        'btn_save': 'Save',
        'btn_save_image': 'Save Image',
        'btn_save_result': 'Show Result',
        'btn_save_para': 'Show Parameters',
        'btn_load_data': 'Load Data',
        'btn_reset': 'Reset',
        'btn_calculate': 'Calculate',
        'btn_predict': 'Predict',
        'btn_switch_2d': 'Switch to 2D',
        'btn_switch_3d': 'Switch to 3D',
        'btn_fill_nan': 'Fill Blanks with 0',
        'btn_remove_nan_cols': 'Remove Columns with Blanks',
        'btn_remove_nan_rows': 'Remove Rows with Blanks',
        'btn_flatten': 'Flatten',
        'btn_open_qapf': 'Open QAPF Diagram',
        'btn_calc_cipw': 'Calculate CIPW Norm',
        'btn_calc_zircon_ce': 'Calculate Zircon Ce',
        'btn_show_result': 'Show Result',
        'btn_save_figure': 'Save Figure',
        'btn_save_results': 'Save Results',
        'btn_cluster_labels': 'Cluster Labels',
        
        # Checkboxes
        'cb_legend': 'Legend',
        'cb_fields': 'Field Labels',
        'cb_show_index': 'Show Index',
        'cb_show_labels': 'Show Labels',
        'cb_regression': 'Regression',
        'cb_value_off': 'Value Off',
        'cb_show_corr': 'Show Correlation Matrix',
        
        # Tabs
        'tab_mole': 'Mole %',
        'tab_weight': 'Weight %',
        'tab_volume': 'Volume %',
        'tab_params': 'Calculated Parameters',
        
        # Info
        'info_load_file': 'Load a data file to begin (CSV or Excel)',
        'info_loaded': 'Loaded:',
        
        # Window titles
        'win_main': 'GeoPyTool Reborn',
        'win_tas': 'TAS Diagram',
        'win_ree': 'REE Diagram',
        'win_trace': 'Trace Element Diagram',
        'win_harker': 'Harker Diagram',
        'win_pearce': 'Pearce Tectonic Diagram',
        'win_qapf': 'QAPF Diagram',
        'win_qfl': 'QFL Diagram',
        'win_pca': 'Principal Component Analysis',
        'win_cluster': 'Cluster Analysis',
        'win_statistics': 'Statistics',
        'win_svm': 'SVM Classification',
        'win_lda': 'LDA Analysis',
        'win_mlp': 'MLP Neural Network',
        'win_rbsr': 'Rb-Sr Isochron Diagram',
        'win_smnd': 'Sm-Nd Isochron Diagram',
        'win_kar': 'K-Ar Isochron Diagram',
        'win_arar': 'Ar-Ar Isochron Diagram',
        'win_cipw': 'CIPW Norm Calculation',
        'win_zircon_ce': 'Zircon Ce Oxygen Fugacity',
        'win_combine': 'Combine Data',
        'win_flatten': 'Flatten Data',
        
        # About
        'about_title': 'About GeoPyTool Reborn',
        'about_version': 'Version:',
        'about_date': 'Date:',
        'about_desc': 'A comprehensive geochemistry data analysis toolkit.',
        'about_restructured': 'Restructured from the original GeoPyTool.',
        'about_website': 'Website:',
        
        # Language
        'lang_en': 'English',
        'lang_zh': '中文',
        'menu_language': 'Language',
    },
    'zh': {
        # Menu
        'menu_file': '文件(&F)',
        'menu_geochemistry': '地球化学(&G)',
        'menu_analysis': '分析(&A)',
        'menu_isotopes': '同位素(&I)',
        'menu_tools': '工具(&T)',
        'menu_help': '帮助(&H)',
        
        # File menu
        'action_open': '打开(&O)...',
        'action_save': '保存(&S)...',
        'action_quit': '退出(&Q)',
        
        # Geochemistry menu
        'action_tas': 'TAS图解',
        'action_ree': '稀土元素蜘蛛图',
        'action_trace': '微量元素图解',
        'action_harker': 'Harker图解',
        'action_pearce': 'Pearce构造判别图解',
        'menu_triangular': '三角形图解',
        'action_qapf': 'QAPF图解',
        'action_qfl': 'QFL图解',
        
        # Analysis menu
        'action_pca': '主成分分析',
        'action_cluster': '聚类分析',
        'action_statistics': '统计',
        'menu_ml': '机器学习',
        'action_svm': 'SVM分类',
        'action_lda': 'LDA分析',
        'action_mlp': 'MLP神经网络',
        'action_pca_ml': 'PCA分析',
        
        # Isotopes menu
        'action_rbsr': 'Rb-Sr等时线',
        'action_smnd': 'Sm-Nd等时线',
        'action_kar': 'K-Ar等时线',
        'action_arar': 'Ar-Ar等时线',
        
        # Tools menu
        'action_cipw': 'CIPW标准矿物计算',
        'action_combine': '数据合并',
        'action_flatten': '数据展平',
        'action_zircon_ce': '锆石Ce氧逸度计算',
        
        # Help menu
        'action_about': '关于(&A)',
        
        # Toolbar
        'toolbar_open': '打开',
        'toolbar_save': '保存',
        'toolbar_tas': 'TAS',
        'toolbar_ree': 'REE',
        'toolbar_trace': 'Trace',
        'toolbar_harker': 'Harker',
        
        # Status
        'status_ready': '就绪',
        'status_loaded': '已加载',
        
        # Dialogs
        'dialog_open_file': '打开数据文件',
        'dialog_save_file': '保存数据文件',
        'dialog_save_image': '保存图像',
        'dialog_save_cipw': '保存CIPW结果',
        'dialog_save_zircon_ce': '保存锆石Ce结果',
        'dialog_save_figure': '保存图像',
        'filter_all': '所有支持的格式 (*.csv *.xlsx *.xls)',
        'filter_csv': 'CSV文件 (*.csv)',
        'filter_excel': 'Excel文件 (*.xlsx *.xls)',
        'filter_png': 'PNG文件 (*.png)',
        'filter_pdf': 'PDF文件 (*.pdf)',
        'filter_svg': 'SVG文件 (*.svg)',
        
        # Messages
        'msg_no_data': '没有数据可保存。',
        'msg_no_results': '没有结果可保存，请先计算。',
        'msg_load_first': '请先加载数据。',
        'msg_save_success': '已保存到',
        'msg_calc_success': '已计算 {} 个样品的CIPW标准矿物。',
        'msg_no_calc': '请先计算CIPW。',
        'msg_zircon_ce_no_result': '没有有效的锆石Ce结果，请检查数据。',
        'msg_zircon_ce_calc_success': '已计算 {} 个样品的锆石Ce4+/Ce3+。',
        'msg_file_saved': '文件保存成功。',
        'msg_error': '错误',
        'msg_warning': '警告',
        'msg_success': '成功',
        
        # Labels
        'label_rows': '行数：',
        'label_columns': '列数：',
        'label_x_axis': 'X轴：',
        'label_y_axis': 'Y轴：',
        'label_diagram': '图解：',
        'label_kernel': '核函数：',
        'label_linkage': '连接方式：',
        'label_distance': '距离：',
        'label_clusters': '聚类数：',
        'label_type': '类型：',
        'label_columns_count': '列数：',
        'label_component': '成分',
        'label_results': '结果：',
        
        # Buttons
        'btn_save': '保存',
        'btn_save_image': '保存图像',
        'btn_save_result': '显示结果',
        'btn_save_para': '显示参数',
        'btn_load_data': '加载数据',
        'btn_reset': '重置',
        'btn_calculate': '计算',
        'btn_predict': '预测',
        'btn_switch_2d': '切换到2D',
        'btn_switch_3d': '切换到3D',
        'btn_fill_nan': '用0填充空白',
        'btn_remove_nan_cols': '删除含空白的列',
        'btn_remove_nan_rows': '删除含空白的行',
        'btn_flatten': '展平',
        'btn_open_qapf': '打开QAPF图解',
        'btn_calc_cipw': '计算CIPW标准矿物',
        'btn_calc_zircon_ce': '计算锆石Ce',
        'btn_show_result': '显示结果',
        'btn_save_figure': '保存图像',
        'btn_save_results': '保存结果',
        'btn_cluster_labels': '聚类标签',
        
        # Checkboxes
        'cb_legend': '图例',
        'cb_fields': '字段标签',
        'cb_show_index': '显示索引',
        'cb_show_labels': '显示标签',
        'cb_regression': '回归线',
        'cb_value_off': '数值关闭',
        'cb_show_corr': '显示相关矩阵',
        
        # Tabs
        'tab_mole': '摩尔百分比',
        'tab_weight': '重量百分比',
        'tab_volume': '体积百分比',
        'tab_params': '计算参数',
        
        # Info
        'info_load_file': '加载数据文件开始（CSV或Excel）',
        'info_loaded': '已加载：',
        
        # Window titles
        'win_main': 'GeoPyTool Reborn',
        'win_tas': 'TAS图解',
        'win_ree': 'REE图解',
        'win_trace': '微量元素图解',
        'win_harker': 'Harker图解',
        'win_pearce': 'Pearce构造判别图解',
        'win_qapf': 'QAPF图解',
        'win_qfl': 'QFL图解',
        'win_pca': '主成分分析',
        'win_cluster': '聚类分析',
        'win_statistics': '统计分析',
        'win_svm': 'SVM分类',
        'win_lda': 'LDA分析',
        'win_mlp': 'MLP神经网络',
        'win_rbsr': 'Rb-Sr等时线图解',
        'win_smnd': 'Sm-Nd等时线图解',
        'win_kar': 'K-Ar等时线图解',
        'win_arar': 'Ar-Ar等时线图解',
        'win_cipw': 'CIPW标准矿物计算',
        'win_zircon_ce': '锆石Ce氧逸度计算',
        'win_combine': '数据合并',
        'win_flatten': '数据展平',
        
        # About
        'about_title': '关于 GeoPyTool Reborn',
        'about_version': '版本：',
        'about_date': '日期：',
        'about_desc': '一个综合性的地球化学数据分析工具包。',
        'about_restructured': '从原始GeoPyTool重构而来。',
        'about_website': '网站：',
        
        # Language
        'lang_en': 'English',
        'lang_zh': '中文',
        'menu_language': '语言',
    }
}


def set_language(lang: str):
    """Set the current language."""
    global _current_lang
    if lang in TRANSLATIONS:
        _current_lang = lang
    else:
        _current_lang = 'en'


def get_language() -> str:
    """Get the current language code."""
    return _current_lang


def tr(key: str, default: str = None) -> str:
    """
    Translate a key to the current language.
    
    Args:
        key: Translation key
        default: Default value if key not found (defaults to key itself)
    
    Returns:
        Translated string
    """
    if default is None:
        default = key
    
    lang_dict = TRANSLATIONS.get(_current_lang, TRANSLATIONS['en'])
    return lang_dict.get(key, TRANSLATIONS['en'].get(key, default))


def get_available_languages() -> list:
    """Get list of available language codes."""
    return list(TRANSLATIONS.keys())


class Translator:
    """
    Translator class for binding to Qt signals.
    
    Usage:
        translator = Translator()
        translator.language_changed.connect(self.update_ui)
    """
    
    _instance = None
    _callbacks = []
    
    def __init__(self):
        if Translator._instance is not None:
            raise RuntimeError("Use Translator.instance()")
        Translator._instance = self
    
    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance
    
    def add_callback(self, callback):
        """Add a callback to be called when language changes."""
        if callback not in self._callbacks:
            self._callbacks.append(callback)
    
    def remove_callback(self, callback):
        """Remove a callback."""
        if callback in self._callbacks:
            self._callbacks.remove(callback)
    
    def set_language(self, lang: str):
        """Set language and notify all callbacks."""
        set_language(lang)
        for callback in self._callbacks:
            try:
                callback()
            except Exception as e:
                print(f"Error in language callback: {e}")