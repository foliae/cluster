class Param(dict):

	def __init__(self,argv,opts):
		self.defaults=opts
		self.initTypes()
		self.process_options(argv)

	def initTypes(self):
		self.types={
				'float':self.initFloat,
				'int':self.initInt,
				'str':self.initStr
				}

	def process_options(self,argv):
		self.set_to_default()
		options=argv

		i=0
		while i<len(options):
			opt=options[i]
			if opt in self.defaults:
				i=i+1
				(val,type,name,attr)=self.defaults[opt]
				self[name]=self.types[type](options[i])
				#print name,self.types[type](options[i])
			else:
				self.help()
				raise ValueError("wrong options")
			i+=1

	def show(self):
		for k in self.keys():
			info=self[k]
			desc='\t%s\n\t\tset to %s'%(k,info)
			print desc

	def help(self):
		for k in self.defaults.keys():
			info=self.defaults[k]
			desc='\t%s\n\t\t%s:%s\n\t\tthe default is set to %s'%(k,info[2],info[3],str(info[0]))
			print desc


	def initFloat(self,s):
		return float(s)

	def initInt(self,s):
		return int(s)

	def initStr(self,s):
		return str(s)


	def set_to_default(self):
		for p in self.defaults.keys():
			(val,type,name,attr)=self.defaults[p]
			self[name]=val
