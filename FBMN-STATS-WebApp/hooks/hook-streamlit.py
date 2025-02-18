from PyInstaller.utils.hooks import copy_metadata

datas = []
datas += copy_metadata("streamlit")
datas += copy_metadata("plotly")
datas += copy_metadata("pingouin")
datas += copy_metadata("openpyxl")
datas += copy_metadata("kaleido")
datas += copy_metadata("scikit_posthocs")
datas += copy_metadata("gnpsdata")
datas += copy_metadata("scikit_learn")
datas += copy_metadata("tabulate")
datas += copy_metadata("networkx")
datas += copy_metadata("pandas_flavor")
datas += copy_metadata("numpy")