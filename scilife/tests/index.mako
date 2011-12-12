<%!
import os
import sys
from mako.template import Template
from mako.lookup import TemplateLookup
mylookup = TemplateLookup(directories=[os.path.abspath('../scilife/templates')])
config = dict( 
   results = "/datad/projects/a2010002/projects/e_hellstrom_11_01/flowcells/111017_AD072NACXX/",
)
# doctemplate = mylookup.get_template("coverage_analysis.mako")
%>

<%namespace name="dt" file="coverage_analysis.mako"/>
${dt.body(config=config)}


