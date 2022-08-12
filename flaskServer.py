from flask import Flask, abort, redirect, request, send_from_directory, Response, render_template, abort, redirect, request, send_from_directory, Response, render_template, make_response, url_for, jsonify
from itemPage import itemPage
from catResults import catSearchResults
from searchResults import searchResults

def APIServer(Valid_Keys):
  app = Flask(import_name=__name__)

  #For getting API current version.
  @app.route('/version')
  def version():
        
        return jsonify({'Version': 1})

  @app.route('/search')
  def search():
      #Gets arguments
      Search_Key = request.args.get("search", "Null")
      key = request.args.get("key", "Null")
      page = request.args.get("page","0")
      if key == "Null" or key not in Valid_Keys:
        abort(403)
      
      if Search_Key == "Null":
        abort(412)
      else:
        results = searchResults(Search_Key,page)
        #print(results)
        return jsonify(results)


  @app.route('/cat')
  def cat():
      #Gets arguments
      search = request.args.get("search", "Null")
      key = request.args.get("key", "Null")
      page = request.args.get("page","0")
      if key == "Null" or key not in Valid_Keys:
        abort(403)
      
      if search == "Null":
        abort(412)
        
      else:
        if search == 'toolstestequipment':
          cat = '/tools-test-equipment/c/7'
        elif search == 'componentselectromechanical':
          cat = '/components-electromechanical/c/2'
        elif search == 'securitysurveillance':
          cat = '/security-surveillance/c/6'
        elif search == 'computingcommunication':
          cat = '/computing-communication/c/3'
        elif search == 'soundvideo':
          cat = '/sound-video/c/8'
        elif search == 'kitssciencelearning':
          cat = '/kits-science-learning/c/9'
        elif search == 'powerbatteries':
          cat = '/power-batteries/c/0'
        elif search == 'outdoorsautomotive':
          cat = '/outdoors-automotive/c/5'
        elif search == 'cablesconnectors':
          cat = '/cables-connectors/c/1'
        elif search == 'hobbiesgadgets':
          cat = '/hobbies-gadgets/c/4'
        else:
          abort(400)
        results = catSearchResults(cat,page)
        #print(results)
        return jsonify(results)

  @app.route('/page')
  def page():
      #Gets arguments
      Product_Code = request.args.get("code", "Null")
      key = request.args.get("key", "Null")
      if key == "Null" or key not in Valid_Keys:
        abort(403)
      
      if Product_Code == "Null":
        abort(412)
      else:
        results = itemPage(Product_Code.upper())
        #print(results)
        return jsonify(results)



  app.run(host='0.0.0.0', port=80)