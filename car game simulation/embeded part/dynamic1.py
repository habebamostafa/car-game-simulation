from flask import Flask, jsonify, render_template,request
import time
import serial
mpdata=serial.Serial("COM4",9600)

time.sleep(2)

mpdata.write("game on\r".encode())

while(1):
    if(mpdata.inWaiting()==0):
        pass
    mpdata.readline()
    break
        


app = Flask(__name__)

@app.route('/_stuff', methods=['GET', 'POST'])
def stuff():
    if request.method == 'POST':
        # Update the server time with the time sent from JavaScript 
        speed = request.json.get('sped')
        rpm = request.json.get('rpm')
        accident = request.json.get('accid')
        
        cmd = str(speed) + ',' + str(accident) + ',' + str(rpm) + '\r\n'
        cmd = cmd.encode()
        mpdata.write(cmd)
    if(mpdata.inWaiting()==0):
        dataPacket = [0,0,0,0,0]
        
    else:
        dataPacket = mpdata.readline()
        dataPacket = str(dataPacket,'utf-8').strip('\r\n').split(',')
        
       
    return jsonify(DATA=dataPacket)


@app.route('/')
def index():

    return render_template('index.html')


if __name__ == '__main__':
    
    app.run()
