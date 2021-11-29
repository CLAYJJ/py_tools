import re
import os
import sys

file_name = os.path.basename(__file__)
current_dir = os.path.dirname(__file__)
default_log_name = "svn.log"
default_log_path = os.path.join(current_dir, default_log_name)


def get_log(start, end, svn_path, log_path=default_log_path):
	"""
	todo 读取excel，将结果写回excel
	svn log -r {start}:{end} -v --diff svn_path > svn.log
	:param log_path: svn日志存储路径
	:param start: 开始时间
	:param end: 结束时间
	:param svn_path: svn路径
	:return:
	"""
	cmd = f"svn log -r {{{start}}}:{{{end}}} -v --diff {svn_path} > {log_path}"
	print(f"执行命令{cmd}")
	os.system(cmd)
	return log_path


def print_usage():
	print(f"usage:python3 {file_name} <svn log path>")


'''全局变量存储最终统计结果'''
result = dict()

def stat(path):
	splitter = f"\n------------------------------------------------------------------------\n"
	#print(f"splitter:{splitter}")
	try:
		"""
		svn提交的日志编码格式为gbk，而java源码文件的编码格式为utf-8，最后输出的日志文件无论以哪种格式打开都会出现乱码
		解决方案：open函数参数中添加errors参数值为ignore即可忽略编码错误，参考：https://docs.python.org/3/library/functions.html#open
		"""
		with open(path, mode="r", encoding="utf-8", errors='ignore') as f:
			buf = f.read()
			buf = "\n"+buf
	except FileNotFoundError as err:
		print(f"文件{path} 不存在")
		return 
	if not re.search(splitter, buf):
		print("svn log文件格式不正确,尝试使用svn log -r {2020-01-03}:{2020-01-10} -v --diff > test.log")
		return
	arr = re.split(splitter, buf)
	for block in arr:
		if block:
			lines = block.split("\n")
			try:
				name = lines[0].split("|")[1]
			except IndexError as err:
				continue
			count = 0
			for line in lines:
				if re.match(r"^[\+]", line) and line.find("+++") != 0 :
					count += 1
			if name in result:
				result[name] += count
			else:
				result[name] = count
			result['total'] = 0
			for value in result.values():
				result['total'] += value
	return result
'''
'''

back_paths = [
'https://172.31.47.240/svn/ZHCSSZZS_Project/branches/code/das',
	]
front_paths = [
	'https://172.31.47.240/svn/ZHCSSZZS_Project/branches/code/vue-dd/src'
]	
if __name__ == "__main__":
	start = "2021-01-01"
	end = "2021-11-22"
	paths = back_paths
	for svn_path in paths:
		log_path = get_log(start, end, svn_path)
		stat(log_path)
	print('最终结果：')
	print(result)