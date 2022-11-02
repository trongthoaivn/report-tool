import os
import json
import base64
from flask import Flask,render_template,session, request, url_for
from flask_session import Session
from helper.helper import create_file_name, find_item_by_key_value, delete_item, create_pdf_file

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
			employee_data = find_item_by_key_value(data,"id", id)
			item["id"] = employee_data["id"]
			item["avatar"] = employee_data["avatar"]
			item["fullName"] = employee_data["fullName"]
			item["bDay"] = employee_data["bDay"]
			item["sex"] = employee_data["sex"]
			item["department"] = employee_data["department"]
			item["nameCard"] = employee_data.get("nameCard")
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
			file =  create_pdf_file(new_employee,template_path="name-card/name-card.xml",remove_file=2)
			if file["code"] != "success":
				raise Exception("create pdf fail")
			new_employee.update({"nameCard" : file["data"]["file_path"]})
			session["data_list"].append(new_employee)
			return {
				"code" : "success",
				"data" : url_for("index")
			}
		except Exception as ex:
			print(ex)
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
			print(ex)
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
				data = session["data_list"]
				employee = find_item_by_key_value(data,"id", id)
				img_path = employee["avatar"]
				pdf_path = employee["nameCard"]
				if employee is None :
					return {
						"code": "fail",
						"message": "not exist item!"
					}
				if delete_item(data, employee, "data_list"):
					os.remove(img_path)
					os.remove(pdf_path)
					return {
						"code" : "success",
						"data" : url_for("index")
					}
				else:
					raise Exception("Delete fail")
			else:
				raise Exception("missing params")
		except Exception as ex:
			print(ex)
			return {
				"code": "fail",
				"message": str(ex)
			}


@app.route('/preview-name-card', methods=["POST"])
def preview_name_card():
	params = request.json
	try:
		if "id" in params:
			id = int(params["id"])
			data = session["data_list"]
			employee = find_item_by_key_value(data,"id", id)
			if employee["nameCard"]	== "":
				file = create_pdf_file(employee,template_path="name-card/name-card.xml")
				if file["code"] == "success":
					return{
						"code" : "success",
						"data" : file["data"]["base64_str"].decode("utf-8") 
					}
				else: 
					raise Exception("create pdf fail")
			else:
				if os.path.exists(employee["nameCard"]):
					file_pdf = open(employee["nameCard"], "rb")
					encoded_string = base64.b64encode(file_pdf.read())
					file_pdf.close()
					return{
						"code" : "success",
						"data" : encoded_string.decode("utf-8") 
					}
				else:
					raise Exception("not exist pdf file!")
		else:
			raise Exception("missing params")
	except Exception as ex:
		print(ex)
		return {
			"code": "fail",
			"message": str(ex)
		}

if __name__ == '__main__':
	app.run(host="0.0.0.0",port=5000,debug=True)
