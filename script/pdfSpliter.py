from PyPDF2 import PdfReader, PdfWriter

# 输入 PDF 文件路径
input_pdf_path = r"D:\Container\Download\Wx\WeChat Files\wxid_xjqgtf34l2hs22\FileStorage\File\2024-12\跨物种单细胞Embedding检索库.pdf"
# 输出 PDF 文件路径
output_pdf_path = r"D:\Container\Download\Wx\WeChat Files\wxid_xjqgtf34l2hs22\FileStorage\File\2024-12\跨物种单细胞Embedding检索库_合并后.pdf"

# 打开 PDF
reader = PdfReader(input_pdf_path)
writer = PdfWriter()

# 获取 PDF 页数
total_pages = len(reader.pages)

# 将第 8 页及以后的内容添加到新的 PDF
for page_num in range(7, total_pages):  # 页码从 7 开始（索引从 0 开始，第 8 页是索引 7）
    page = reader.pages[page_num]
    writer.add_page(page)

# 保存到新的 PDF 文件
with open(output_pdf_path, "wb") as output_pdf:
    writer.write(output_pdf)

print(f"新的 PDF 文件已生成：{output_pdf_path}")