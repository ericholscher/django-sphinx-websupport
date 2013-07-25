import json

from .backend import DjangoStorage
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
from sphinx.websupport import WebSupport

storage = DjangoStorage()

support = WebSupport(
        srcdir='/Users/eric/projects/readthedocs.org/docs',
        builddir='/Users/eric/projects/readthedocs.org/docs/_build/websupport',
        datadir='/Users/eric/projects/readthedocs.org/docs/_build/websupport/data',
        storage=storage,
        docroot='websupport',
    )


def jsonify(obj, jsonp=False):
    if jsonp:
        return HttpResponse("%s(%s)" % (jsonp, json.dumps(obj)), mimetype='text/javascript')
    else:
        return HttpResponse(json.dumps(obj), mimetype='text/javascript')

########
# called by javascript
########
def get_comments(request):
    username = None
    node_id = request.GET.get('node', '')
    jsonp = request.GET.get('callback', None)
    data = support.get_data(node_id, username=username)
    return jsonify(data, jsonp=jsonp)

def get_options(request):
    jsonp = request.GET.get('callback', None)
    return jsonify(support.base_comment_opts, jsonp=jsonp)

def get_metadata(request):
    document = request.GET.get('document', '')
    jsonp = request.GET.get('callback', None)
    return jsonify(storage.get_metadata(docname=document), jsonp=jsonp)

@csrf_exempt
def add_comment(request):
    parent_id = request.POST.get('parent', '')
    node_id = request.POST.get('node', '')
    text = request.POST.get('text', '')
    proposal = request.POST.get('proposal', '')
    username = None
    comment = support.add_comment(text=text, node_id=node_id,
                                  parent_id=parent_id,
                                  username=username, proposal=proposal)
    return jsonify(comment)


#######
# Normal Views
#######

def build(request):
    support.build()

def serve_file(request, file):
    document = support.get_document(file)

    return render_to_response('doc.html',
                              {'document': document},
                              context_instance=RequestContext(request))

######
# Called by Builder
######

def has_node(request):
    node_id = request.GET.get('node_id', '')
    exists = storage.has_node(node_id)
    return jsonify({'exists': exists})

@csrf_exempt
def add_node(request):
    post_data = json.loads(request.raw_post_data)
    document = post_data.get('document', '')
    id = post_data.get('id', '')
    source = post_data.get('source', '')
    created = storage.add_node(id, document, source)
    return jsonify({'created': created})
