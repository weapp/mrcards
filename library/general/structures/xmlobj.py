class filter_by_id:
	def __init__(self, id):
		self.id=id
	def __call__(self, obj):
		if obj.attr.has_key('id'):
			return obj.attr['id']==self.id
		else:
			return False

class filter_by_class:
	def __init__(self, name):
		self.name=name
	def __call__(self, obj):
		if obj.attr.has_key('class'):
			return self.name in obj.attr['class'].split(' ')
		else:
			return False

class filter_by_tagname:
	def __init__(self, name):
		self.name=name
	def __call__(self, obj):
		return obj.tagname==self.name
		
class filter_completo:
	def __init__(self,exp):
		dic=self.parsear_exp(exp)
		self.filters=[]
		if dic.has_key('tag'):
			self.filters.append(filter_by_tagname(dic['tag']))
		if dic.has_key('id'):
			self.filters.append(filter_by_id(dic['id']))
		if dic.has_key('class'):
			self.filters.append(filter_by_class(dic['class']))
	
	def __call__(self,obj):
		r=True
		for filter in self.filters:
			r &= filter(obj)
		return r
	
	
	def parsear_exp(self,exp):
		pnt=exp.find('.')
		shr=exp.find('#')
		if exp.startswith('#'):
			if pnt!=-1:
				r={'id':exp[1:pnt]}
				r['class']=self.parsear_exp(exp[pnt:])['class']
			else:
				r={'id':exp[1:]}
		elif exp.startswith('.'):
			if shr!=-1:
				r={'class':exp[1:shr]}
				r['id']=self.parsear_exp(exp[shr:])['id']
			else:
				r={'class':exp[1:]}
		else:
			if max(shr, pnt)==-1:#no tiene # ni .
				r={'tag':exp}
			else:#tiene al menos # o .
				if min(shr, pnt)!=-1:#tiene # y .
					r={'tag':exp[:min(shr, pnt)]}
					r.update(self.parsear_exp(exp[min(shr, pnt):]))
				else: #solo tiene uno de los dos
					r={'tag':exp[:max(shr, pnt)]}
					r.update(self.parsear_exp(exp[max(shr, pnt):]))
		return r
		
	

class Tag(list):
	AUTO=0
	SIMPLE=1
	DOUBLE=2
	
	def filter_objects(self, filter=lambda x:True):
		r=[]
		for obj in self:
			if isinstance(obj, Tag):
				if filter(obj):
					r.append(obj)
				r.extend(obj.filter_objects(filter))
		return r
		
	def get_by_tagname(self,name):
		return self.filter_objects(filter=filter_by_tagname(name))
		
	def get_by_class(self,name):
		return self.filter_objects(filter=filter_by_class(name))
		
	def get_by_id(self,id):
		r=self.filter_objects(filter=filter_by_id(id))
		return [r[0]] if r else []
		
	def get(self,expresion):
		expr=expresion.split(' ')
		exp=expr[0]
		resultados=self.filter_objects(filter=filter_completo(exp))
		
		if len(expr)>1:
			r=[]
			for result in resultados:
				r.extend(result.get(' '.join(expr[1:])))
			resultados=r
		return resultados
		
	def __init__(self, tagname,attrs=None,childs=None,pre="",pos=""):
		attrs={} if attrs is None else attrs.copy()
		childs=[] if childs is None else childs[:]
		list.__init__(self,childs)
		self.type=Tag.AUTO
		self.tagname=tagname
		self.attr=attrs
		self.pre=pre
		self.pos=pos
		
	def str_attr(self):
		str_attr=''
		for key,value in self.attr.items():
			str_attr+=" " + str(key) + "=\"" + str(value) + "\""
		return str_attr
	
	def str_contenido(self):
		contenido="\n"+"\n".join(map(str,self))
		contenido=contenido.replace("\n","\n\t",)
		return contenido
	
	def __str__(self):
		if self.type==Tag.DOUBLE or (self.type==Tag.AUTO and len(self)!=0):
			s="<%(tagname)s%(attrs)s>%(content)s\n</%(tagname)s>" % dict(tagname=self.tagname,attrs=self.str_attr(),content=self.str_contenido())
		elif self.type==Tag.SIMPLE or (self.type==Tag.AUTO and len(self)==0):
			s="<%s%s/>" % (self.tagname,self.str_attr())
		return str(self.pre)+s+str(self.pos)
		
	def __repr__(self):
		return str(self)
		
class Contenedor(Tag):
	def __init__(self, tagname,*args,**keys):
		Tag.__init__(self,tagname,*args,**keys)
		self.type=Tag.DOUBLE
		
class Html(Contenedor):
	def __init__(self,*args,**keys):
		Contenedor.__init__(self,'html',*args,**keys)
		
class Body(Contenedor):
	def __init__(self,*args,**keys):
		Contenedor.__init__(self,'body',*args,**keys)
		
class Head(Contenedor):
	def __init__(self,*args,**keys):
		Contenedor.__init__(self,'head',*args,**keys)
		
class Div(Contenedor):
	def __init__(self,*args,**keys):
		Contenedor.__init__(self,'div',*args,**keys)
		
class Span(Contenedor):
	def __init__(self,*args,**keys):
		Contenedor.__init__(self,'span',*args,**keys)
		
if __name__=="__main__":
	html=Html(childs=[
		Body(childs=[
			Div({'class':'a','id':'aidi'},
				[
				'[contenido 1]',
							Div(childs=[
				'contenido 3',
				Span(childs=['contenido 4'])
				]),
				'[contenido 2]'
				]
				),
			Div(childs=[
				'contenido 3',
				Span(childs=['contenido 4'])
				])
			])
		])

	ht=Html({"xmlns":"http://www.w3.org/1999/xhtml","lang":"es_ES",'xml:lang':"es_ES"},
		[
			Head({}, 
				[
					Tag("meta",{'http-equiv':"Content-type","content":"text/html; charset=utf-8"})
				]			
			)
		],
		pre='''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">'''
	)
	
	import os
	os.system('cls')
	#print html
	#print
	#print ht
	
	for obj in html.get('.a#aidi'):
		print str(obj) +"\n\n------\n"

	raw_input()