import random
from flask import Flask, render_template, request, send_file
import io

app = Flask(__name__)

@app.route('/')
def hello():
    return render_template('index.html', output=None)

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        customer_name = request.form.get('customer_name') 
        day_of_week = request.form.get('day_of_week')  
        amt_corn = float(request.form.get('amt_corn'))  
        distance = float(request.form.get('distance'))  
        
        charge_per_mile = 0.50
        
        total_transportation_cost = distance * charge_per_mile
        
        quality = random.uniform(0.01, 0.02)  # random quality control check
        
        effective_corn = amt_corn * (1 - quality)  # amount of corn 

        cost_per_lb = 0.5
        total_price = total_transportation_cost + (amt_corn * cost_per_lb)

    except (ValueError, TypeError):
        output = "Invalid input. Please enter numeric values."
        effective_corn = None
        total_transportation_cost = None
        total_price = None
        cost_per_lb = None
        customer_name = None
    else:
        output = "Receipt created successfully."

        receipt_info = f"""Receipt
        Customer Name: {customer_name}
        Day of the Week: {day_of_week}
        Total Amount of Effective Corn (after quality control): {round(effective_corn, 2) if effective_corn else 0} lb
        Transportation Cost ($ per mile): ${round(charge_per_mile, 2)}
        Total Transportation Cost: ${round(total_transportation_cost, 2) if total_transportation_cost else 0}
        Cost per lb: ${round(cost_per_lb, 2)}
        Total Amount Owed: ${round(total_price, 2) if total_price else 0}
        """

        buffer = io.StringIO()
        buffer.write(receipt_info)
        buffer.seek(0)  
    
    return render_template(
        'index.html', 
        output=output, 
        customer_name=customer_name,
        day_of_week=day_of_week,
        effective_corn=round(effective_corn, 2) if effective_corn else None,
        transportation_cost_per_mile=round(charge_per_mile, 2),
        total_transportation_cost=round(total_transportation_cost, 2) if total_transportation_cost else None,
        total_price=round(total_price, 2) if total_price else None,
        cost_per_lb=round(cost_per_lb, 2) if cost_per_lb else None,
        receipt_buffer=buffer.getvalue()  
    )


@app.route('/download')
def download():

    receipt_info = request.args.get('receipt', '')
    buffer = io.StringIO()
    buffer.write(receipt_info)
    buffer.seek(0)
    
    return send_file(io.BytesIO(buffer.getvalue().encode()), 
                     as_attachment=True, 
                     download_name='receipt.txt',  
                     mimetype='text/plain')


if __name__ == '__main__':
    app.run()
