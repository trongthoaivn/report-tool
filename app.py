import os
import json
from flask import Flask,render_template,session, request, url_for
from flask_session import Session

app = Flask(__name__,template_folder='templates')
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config["UPLOAD_FOLDER"] = "static/images/upload"
Session(app)

@app.route('/home')
@app.route('/', methods=["GET"])
def index():
	"""_summary_

	Returns:
		_type_: _description_
	"""
	if "data_list" not in session:
		session["data_list"] = []
	return render_template("index.html", data_list = session["data_list"])

@app.route('/manage', methods=["GET","POST","PUT","DELETE"])
def manage_data():
	"""_summary_

	Returns:
		_type_: _description_
	"""
	# GET
	if request.method == 'GET':
		params = request.args
		title = "Register Employee"
		buttons = ["Register"] 
		item = {
				"id":'',
				"avatar":'',
				"fullName":'',
				"bDay":'',
				"sex":'',
				"department":'',
				"nameCard":''
			}
		if "id" in params:
			data = session.get("data_list")
			id = int(params["id"])
			if data[id] in data: 
				item["id"] = data[id]["id"]
				item["avatar"] = data[id]["avatar"]
				item["fullName"] = data[id]["fullName"]
				item["bDay"] = data[id]["bDay"]
				item["sex"] = data[id]["sex"]
				item["department"] = data[id]["department"]
				item["nameCard"] = data[id]["nameCard"]
				title = "Edit Employee"	
			buttons = ["Save","Delete"] 
		return render_template("manage.html", data_item = item , title = title, buttons = buttons)
	
	# POST
	if request.method == 'POST':
		json_data = request.form.get("data")
		img = request.files.get("file")
		try:
			if json_data is None or img is None:
				raise Exception("Some field not been entered!")
			img.save(os.path.join(app.config['UPLOAD_FOLDER'], img.filename))
			new_employee = json.loads(json_data)
			new_employee.update({"id" : len(session["data_list"]) + 1})
			new_employee.update({"avatar" : os.path.join(app.config['UPLOAD_FOLDER'], img.filename)})
			session["data_list"].append(new_employee)
			return {
				"code" : "success",
				"data" : url_for("index")
			}
		except Exception as ex:
			return {
				"code": "fail",
				"message": str(ex)
			}

	# PUT
	if request.method == 'PUT':
		params = request.args
		data = request.form
		try:
			if "id" in params:
				id = int(params["id"])
				if data[id] in data: 
					item["id"] = id
					item["avatar"] = data[id]["avatar"]
					item["fullName"] = data[id]["fullName"]
					item["bDay"] = data[id]["bDay"]
					item["sex"] = data[id]["sex"]
					item["department"] = data[id]["department"]
					item["nameCard"] = data[id]["nameCard"]
				return {
					"code" : "success",
				}
			else:
				return {
				"code": "fail",
				"message": "not exist item!"
			}
		except Exception as ex:
			return {
				"code": "fail",
				"message": str(ex)
			}

	# DELETE
	if request.method == 'DELETE':
		params = request.args
		try:
			if "id" in params:
				id = int(params["id"])
				session["data_list"].pop(id)
				return {
					"code" : "success",
				}
			else:
				return {
					"code": "fail",
					"message": "not exist item!"
				}
		except Exception as ex:
			return {
				"code": "fail",
				"message": str(ex)
			}


if __name__ == '__main__':
	app.run(host="0.0.0.0",port=5000,debug=True)
