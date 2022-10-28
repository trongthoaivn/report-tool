from turtle import title
from flask import Flask,render_template,session, request
from flask_session import Session

app = Flask(__name__,template_folder='templates')
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
@app.route('/', methods=["GET"])
def index():
	if "data_list" not in session:
		session["data_list"] = []
	item = {
				"id":'',
				"avatar":'',
				"fullName":'',
				"bDay":'',
				"sex":'male',
				"department":'',
				"nameCard":''
			}
	session["data_list"].append(item)
	return render_template("index.html", data_list = session["data_list"])

@app.route('/manage', methods=["GET","POST","PUT","DELETE"])
def manage_data():
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
	if request.method == 'POST':
		form = request.form
		img = request.form
		try:
			session["data_list"].append(form)
			return {
				"code" : "success",
			}
		except Exception as e:
			return{
				"code": "fail",
				"message": e
			}
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
				return{
				"code": "fail",
				"message": "not exist item!"
			}
		except Exception as e:
			return{
				"code": "fail",
				"message": e
			}
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
				return{
					"code": "fail",
					"message": "not exist item!"
				}
		except Exception as e:
			return{
				"code": "fail",
				"message": e
			}
# main driver function
if __name__ == '__main__':
	app.run(host="0.0.0.0",port=80,debug=True)