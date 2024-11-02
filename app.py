import random
from flask import Flask, render_template, request, send_file
import io
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def hello():
    return render_template('index.html', image_path="static/Corn.png" )


from datetime import datetime

@app.route('/calculate', methods=['POST'])
def calculate():
    try:
        customer_name = request.form.get('customer_name') 
        day_of_week = request.form.get('day_of_week')  
        crop_type = request.form.get('crop_type')  
        amt_crop = float(request.form.get('amt_crop'))  
        distance = float(request.form.get('distance'))  
        
        charge_per_mile = 0.50
        total_transportation_cost = distance * charge_per_mile

        quality = random.uniform(0.01, 0.02)  
        effective_crop = amt_crop * (1 - quality)
        image_path = "static/cornSmall.png" 
        if crop_type == 'corn':
            cost_per_lb = 0.5
            image_path = "static/cornSmall.png"
        elif crop_type == 'carrots':
            cost_per_lb = 0.4  
            image_path = "static/carrotSmall.png"
        elif crop_type == 'potatoes':
            cost_per_lb = 0.6  
            image_path = "static/potatoSmall.png"
        else:
            effective_crop = 0
             

        total_price = total_transportation_cost + (effective_crop * cost_per_lb)

        current_time = datetime.now()
        current_date = current_time.strftime('%Y-%m-%d')
        current_time_str = current_time.strftime('%I:%M:%S %p') 
    except (ValueError, TypeError):
        output = "Invalid input. Please enter numeric values."
        effective_crop = None
        total_transportation_cost = None
        total_price = None
        cost_per_lb = None
        customer_name = None
        image_path = "static/Corn.png"
    else:
        output = "Receipt created successfully."
        
        receipt_info = f"""Receipt
        Customer Name: {customer_name}
        Date (YYYY-MM-DD): {current_date}
        Time: {current_time_str}
        Day of the Week: {day_of_week}
        Crop Type: {crop_type.capitalize()}
        Total Amount of Effective Crop (after quality control): {round(effective_crop, 2) if effective_crop else 0} lb
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
        current_date=current_date,
        current_time=current_time_str,  
        customer_name=customer_name,
        day_of_week=day_of_week,
        crop_type=crop_type,
        effective_crop=round(effective_crop, 2) if effective_crop else None,
        transportation_cost_per_mile=round(charge_per_mile, 2),
        total_transportation_cost=round(total_transportation_cost, 2) if total_transportation_cost else None,
        total_price=round(total_price, 2) if total_price else None,
        cost_per_lb=round(cost_per_lb, 2) if cost_per_lb else None,
        receipt_buffer=buffer.getvalue(),
        image_path=image_path  
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
