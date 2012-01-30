from flask import Flask, request
app = Flask(__name__)

import os
import datetime

# Set this offset to the first radio you want to override
radio_offset = 1

@app.route('/say', methods=['GET', 'POST'])
def say_three(line1,line2,line3):
  timestamp = datetime.datetime.now().strftime("%y/%m/%d %H:%M")
  if request.method == 'POST':
    lines = [request.form['line1'], request.form['line2'], request.form['line3']]
  else:
    lines = [request.args.get('line1', ''), request.args.get('line2', ''), request.args.get('line3', '')]
  spaces = ['  ', ' ', '']

  for i in range(len(lines)):
    os.system("echo [%s] %s >> history.log" % (timestamp, lines[i]))
    os.system("tail -n1 history.log")
    os.system("uci set wireless.@wifi-iface[%d].ssid='-%d %s'" % (i+radio_offset,i,lines[i]))

  os.system("uci commit wireless")
  os.system("ifup wan")
  os.system("wifi")

  return "At %s, you said %s, %s, %s" % (timestamp, lines[1], lines[2], lines[3])

if __name__ == "__main__":
  app.run(port=8888,host='0.0.0.0',debug=True)