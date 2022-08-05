function validateForm() {
    var x = document.forms["myForm"]["firstName"].value;
    if (x == "") {
      alert("Please fill out a first name.");
      return false;
    }
  }


function checkPassword(str)
{
    var re = /^(?=.*\d)(?=.*[!@#$%^&*])(?=.*[a-z])(?=.*[A-Z]).{7,}$/;
    return re.test(str);
}




@app.route("/userprofile")
def userprofile():
    return("i am here")
    #cursor.execute("select * from x where course=x")
    #value=cursor.fetchall()
    #return render_template("userprofile.html", data=value, name=x)

#this is routing the url of the flask app
@app.route("/", methods=['POST', 'GET'])
def index():
    if request.method == "POST":
        print(type(request.get_data("audio_data")))
        #f = open('./file.wav', 'wb')
        #f.write(request.get_data("audio_data"))
        #f.close()
        
        if os.path.isfile('./file.wav'):
            print("./file.wav exists")

        return render_template('index.html', request="POST")   
    else:
        return render_template("index.html")