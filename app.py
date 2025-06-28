# app.py
from csv import excel_tab

from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import pymysql
from functools import wraps
import hashlib

import os
import subprocess
from werkzeug.utils import secure_filename
from flask import send_file
import logging
import secrets
from datetime import datetime


# logging.basicConfig(filename='restore_errors.log', level=logging.ERROR)


mgrType = {'系统管理员': "root", '药品管理员': "pharmacy_mgr", '医生': "doctor", '收费员': "cashier", '科室负责人': "dept_head"}


app = Flask(__name__)
app.secret_key = secrets.token_hex(32)

# 备份文件存储路径（确保该路径有写入权限）
BACKUP_DIR = 'backups'
if not os.path.exists(BACKUP_DIR):
    os.makedirs(BACKUP_DIR)

# 允许上传的文件扩展名
ALLOWED_EXTENSIONS = {'sql'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# 数据库配置
DB_CONFIG = {
    'host': 'localhost',
    'port': 3306,
    # 'user': 'dept_head',
    # 'password': 'DeptHeadPassword123',
    'db': 'HospitalManagement',
    'charset': 'utf8mb4'
}

def get_db_connection():
    return pymysql.connect(**DB_CONFIG, cursorclass=pymysql.cursors.DictCursor)

# 密码加密函数
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# 登录限制装饰器
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('请先登录', 'warning')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

# 用户注册
@app.route('/register', methods=['GET', 'POST'])
def register():
    if 'user_id' in session:
        return redirect(url_for('index'))
    if not 'dbpwd' in session:
        return redirect(url_for('connection'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if password != confirm_password:
            flash('两次输入的密码不一致', 'danger')
            return render_template('register.html')

        # 密码强度验证
        if len(password) < 8:
            flash('密码长度必须至少为8个字符', 'danger')
            return render_template('register.html')

        # 用户名格式验证
        if not username.isalnum() or len(username) < 2:
            flash('用户名必须至少2个字符，且只能包含字母和数字', 'danger')
            return render_template('register.html')

        hashed_password = hash_password(password)

        conn = get_db_connection()
        cursor = conn.cursor()
        # 检查用户名是否存在
        cursor.execute("SELECT id FROM users WHERE username=%s", (username,))
        if cursor.fetchone():
            flash('用户名已存在', 'danger')
            cursor.close()
            conn.close()
            return render_template('register.html')

        try:
            # 插入新用户
            cursor.execute("INSERT INTO users(username, password) VALUES(%s, %s)",
                         (username, hashed_password))
            conn.commit()
            flash('注册成功，请登录', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            conn.rollback()
            flash('注册失败，请稍后重试', 'danger')
        finally:
            cursor.close()
            conn.close()

    return render_template('register.html')

# 数据库登录
@app.route('/connection', methods=['GET', 'POST'])
def connection():
    if 'dbpwd' in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        usertype = mgrType[request.form['usertype']]
        dbpwd = request.form['dbpwd']

        DB_CONFIG['user'] = usertype
        DB_CONFIG['password'] = dbpwd

        try:
            conn = get_db_connection()
            cursor = conn.cursor()
        except Exception as e:
            flash('数据库连接失败，请重新输入类型密码', 'danger')
            return redirect(url_for('connection'))
        cursor.close()
        conn.close()

        session['dbpwd'] = dbpwd
        flash('登录成功', 'success')
        return redirect(url_for('login'))
    return render_template('connection.html')

# 用户登录
@app.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('index'))
    if not 'dbpwd' in session:
        return redirect(url_for('connection'))

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = hash_password(password)
        try:
            conn = get_db_connection()
            cursor = conn.cursor()
        except Exception as e:
            flash('数据库连接失败，请重新输入类型密码', 'danger')
            return redirect(url_for('connection'))

        try:
            cursor.execute("SELECT id, password FROM users WHERE username=%s", (username,))
            user = cursor.fetchone()

            if user and user['password'] == hashed_password:
                session['user_id'] = user['id']
                session['username'] = username
                flash('登录成功', 'success')
                return redirect(url_for('index'))
            else:
                flash('用户名或密码错误', 'danger')
        except Exception as e:
            flash('登录失败，请稍后重试', 'danger')
        finally:
            cursor.close()
            conn.close()

    return render_template('login.html')

# 退出登录
@app.route('/logout')
@login_required
def logout():
    session.clear()
    DB_CONFIG.pop('user')
    DB_CONFIG.pop('password')
    flash('已安全退出登录', 'info')
    return redirect(url_for('connection'))

# 首页
@app.route('/')
@login_required
def origin():
    return redirect(url_for('connection'))

@app.route('/index')
@login_required
def index():
    userpwd = session.get('dbpwd')
    if userpwd == '123456':
        return render_template('index.html')
    elif userpwd == 'PharmacyMgr123':
        return render_template('index_pharm.html')
    elif userpwd == 'DoctorPassword123':
        return render_template('index_doctor.html')
    elif userpwd == 'CashierPassword123':
        return render_template('index_cashier.html')
    else:
        return render_template('index_depthead.html')

# 错误网页
# 这是关键部分：定义404错误处理器
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html')
# ------------------------------------------------
# 以下为各模块示例路由及功能，需根据实际需求补充完善
# ------------------------------------------------

# 药品类型管理
@app.route('/medicine_types')
@login_required
def medicine_types():
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT 类型ID, 类型名称, 描述 FROM 药品类型")
    except Exception as e:
        flash('没有权限！', 'danger')
        return redirect(url_for('index'))
    types = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('medicine_types.html', types=types)

@app.route('/medicine_types/add', methods=['GET', 'POST'])
@login_required
def add_medicine_type():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO 药品类型(类型名称, 描述) VALUES(%s, %s)", (name, description))
        except Exception as e:
            flash('没有权限！', 'danger')
            return redirect(url_for('medicine_types'))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('medicine_types'))
    return render_template('add_medicine_type.html')

# 药品信息管理
@app.route('/medicines', methods=['GET', 'POST'])
@login_required
def medicines():
    conn = get_db_connection()
    cursor = conn.cursor()
    drug_stats = []
    if request.method == 'POST':
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
        if not start_date or not end_date:
            flash('请输入开始日期和结束日期', 'danger')
            return redirect(url_for('medicines'))
        try:
            # 将日期字符串转换为 datetime 对象
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

            if start_date > end_date:
                flash('开始日期不能晚于结束日期', 'danger')
                return redirect(url_for('medicines'))

            # 调用药品销售统计存储过程
            cursor.execute("CALL 药品销售统计(%s, %s)", [start_date, end_date])
            drug_stats = cursor.fetchall()

        except Exception as e:
            flash(f'查询失败：{str(e)}', 'danger')



    try:
        cursor.execute("SELECT y.药品ID, y.药品名称, l.类型名称, y.规格, y.单位, y.生产厂家, y.价格, y.库存量 FROM 药品信息 y JOIN 药品类型 l ON y.类型ID=l.类型ID")
        medicines = cursor.fetchall()
        cursor.execute("SELECT * FROM 药品库存视图")
        total_stocks = cursor.fetchall()
        cursor.execute("SELECT * FROM hospitalmanagement.库存预警")
        warnings = cursor.fetchall()
    except Exception as e:
        flash('没有权限！', 'danger')
        return redirect(url_for('index'))
    if 'cursor' in locals():
        cursor.close()
    if 'conn' in locals():
        conn.close()
    return render_template('medicines.html', medicines=medicines, total_stocks=total_stocks, warnings=warnings, drug_stats=drug_stats)

@app.route('/medicines/add', methods=['GET', 'POST'])
@login_required
def add_medicine():
    conn = get_db_connection()
    cursor = conn.cursor()
    if request.method == 'POST':
        name = request.form['name']
        type_id = request.form['type_id']
        spec = request.form['spec']
        unit = request.form['unit']
        manufacturer = request.form['manufacturer']
        price = request.form['price']
        conn_insert = get_db_connection()
        cursor_insert = conn_insert.cursor()
        try:
            cursor_insert.execute("INSERT INTO 药品信息(药品名称, 类型ID, 规格, 单位, 生产厂家, 价格) VALUES(%s, %s, %s, %s, %s, %s)",
                              (name, type_id, spec, unit, manufacturer, price))

        except Exception as e:
            flash('没有权限！', 'danger')
            return redirect(url_for('add_medicine'))
        conn_insert.commit()
        cursor_insert.close()
        conn_insert.close()
        return redirect(url_for('medicines'))

    try:
        cursor.execute("SELECT 类型ID, 类型名称 FROM 药品类型")
    except Exception as e:
        flash('没有权限！', 'danger')
        return redirect(url_for('medicines'))
    types = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('add_medicine.html', types=types)

# 科室管理
@app.route('/departments', methods=['GET', 'POST'])
@login_required
def departments():
    conn = get_db_connection()
    cursor = conn.cursor()
    dept_stats=[]
    if request.method == 'POST':
        start_date = request.form['start_date']
        end_date = request.form['end_date']

        if not start_date or not end_date:
            flash('请输入开始日期和结束日期', 'danger')
            return redirect(url_for('departments'))
        try:
            # 将日期字符串转换为 datetime 对象
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()

            if start_date > end_date:
                flash('开始日期不能晚于结束日期', 'danger')
                return redirect(url_for('departments'))

            conn = get_db_connection()
            cursor = conn.cursor()

            # 调用科室就诊统计存储过程
            cursor.execute("CALL 科室就诊统计(%s, %s)", (start_date, end_date))

            # 获取存储过程的结果集
            dept_stats = cursor.fetchall()


        except Exception as e:
            flash(f'查询失败：{str(e)}', 'danger')


    try:
        cursor.execute("SELECT 科室ID, 科室名称, 负责人, 描述 FROM 科室")
    except Exception as e:
        flash(f'没有权限！{str(e)}', 'danger')
        return redirect(url_for('index'))
    departments = cursor.fetchall()
    if 'cursor' in locals():
        cursor.close()
    if 'conn' in locals():
        conn.close()
    return render_template('departments.html', departments=departments, dept_stats=dept_stats)

@app.route('/departments/add', methods=['GET', 'POST'])
@login_required
def add_department():
    if request.method == 'POST':
        name = request.form['name']
        leader = request.form['leader']
        description = request.form['description']
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO 科室(科室名称, 负责人, 描述) VALUES(%s, %s, %s)",
                       (name, leader, description))
        except Exception as e:
            flash('没有权限！', 'danger')
            return redirect(url_for('prescriptions'))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('departments'))
    return render_template('add_department.html')

# 医生管理
@app.route('/doctors')
@login_required
def doctors():
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT d.医生ID, d.姓名, d.性别, d.职称, k.科室名称, d.联系电话, d.入职日期 FROM 医生 d LEFT JOIN 科室 k ON d.所属科室ID=k.科室ID")
    except Exception as e:
        flash('没有权限！', 'danger')
        return redirect(url_for('index'))
    doctors = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('doctors.html', doctors=doctors)

@app.route('/doctors/add', methods=['GET', 'POST'])
@login_required
def add_doctor():
    conn = get_db_connection()
    cursor = conn.cursor()
    if request.method == 'POST':
        name = request.form['name']
        gender = request.form['gender']
        title = request.form['title']
        department_id = request.form['department_id']
        phone = request.form['phone']
        hire_date = request.form['hire_date']
        conn_insert = get_db_connection()
        try:
            cursor.execute("""
                INSERT INTO 医生(姓名, 性别, 职称, 所属科室ID, 联系电话, 入职日期) 
                VALUES(%s, %s, %s, %s, %s, %s)
            """, (name, gender, title, department_id, phone, hire_date))
            conn.commit()
            flash('医生信息添加成功！', 'success')
            return redirect(url_for('doctors'))
        except Exception as e:
            conn.rollback()
            flash('添加失败：' + str(e), 'danger')

    # 获取所有科室信息供选择
    cursor.execute("SELECT 科室ID, 科室名称 FROM 科室")
    departments = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('add_doctor.html', departments=departments)

@app.route('/doctors/edit/<int:doctor_id>', methods=['GET', 'POST'])
@login_required
def edit_doctor(doctor_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        name = request.form['name']
        gender = request.form['gender']
        title = request.form['title']
        department_id = request.form['department_id']
        phone = request.form['phone']
        hire_date = request.form['hire_date']

        try:
            cursor.execute("""
                UPDATE 医生 
                SET 姓名=%s, 性别=%s, 职称=%s, 所属科室ID=%s, 联系电话=%s, 入职日期=%s 
                WHERE 医生ID=%s
            """, (name, gender, title, department_id, phone, hire_date, doctor_id))
            conn.commit()
            flash('医生信息更新成功！', 'success')
            return redirect(url_for('doctors'))
        except Exception as e:
            conn.rollback()
            flash('更新失败：' + str(e), 'danger')
            return render_template('edit_doctor.html', doctor=request.form)

    # 获取医生信息
    cursor.execute("""
        SELECT d.*, k.科室名称 
        FROM 医生 d 
        LEFT JOIN 科室 k ON d.所属科室ID=k.科室ID 
        WHERE d.医生ID=%s
    """, (doctor_id,))
    doctor = cursor.fetchone()

    if doctor is None:
        flash('医生不存在！', 'danger')
        return redirect(url_for('doctors'))

    # 获取所有科室信息供选择
    cursor.execute("SELECT 科室ID, 科室名称 FROM 科室")
    departments = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('edit_doctor.html', doctor=doctor, departments=departments)

@app.route('/doctors/delete/<int:doctor_id>', methods=['DELETE'])
@login_required
def delete_doctor(doctor_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # 首先检查是否存在关联的处方
        cursor.execute("SELECT COUNT(*) as count FROM 处方 WHERE 医生ID=%s", (doctor_id,))
        result = cursor.fetchone()
        if result['count'] > 0:
            return jsonify({'success': False, 'message': '该医生有关联的处方记录，无法删除！'})

        # 如果没有关联处方，则删除医生
        cursor.execute("DELETE FROM 医生 WHERE 医生ID=%s", (doctor_id,))
        conn.commit()
        return jsonify({'success': True, 'message': '医生删除成功！'})
    except Exception as e:
        conn.rollback()
        return jsonify({'success': False, 'message': str(e)})
    finally:
        cursor.close()
        conn.close()

# 病人管理
@app.route('/patients')
@login_required
def patients():
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT 病人ID, 姓名, 性别, 出生日期, 联系电话, 住址, 医保卡号 FROM 病人")
        patients = cursor.fetchall()
    except Exception as e:
        flash('没有权限！', 'danger')
        return redirect(url_for('index'))
    cursor.close()
    conn.close()
    return render_template('patients.html', patients=patients)

@app.route('/patients/add', methods=['GET', 'POST'])
@login_required
def add_patient():
    if request.method == 'POST':
        name = request.form['name']
        gender = request.form['gender']
        birth_date = request.form['birth_date']
        phone = request.form['phone']
        address = request.form['address']
        card_number = request.form['card_number']
        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute("""
                INSERT INTO 病人(姓名, 性别, 出生日期, 联系电话, 住址, 医保卡号) 
                VALUES(%s, %s, %s, %s, %s, %s)
            """, (name, gender, birth_date, phone, address, card_number or None))
            conn.commit()
            flash('病人信息添加成功！', 'success')
            return redirect(url_for('patients'))
        except Exception as e:
            conn.rollback()
            # flash('添加失败：' + str(e), 'danger')
            flash('添加失败：没有权限！', 'danger')
        finally:
            cursor.close()
            conn.close()
    return render_template('add_patient.html')

@app.route('/patients/edit/<int:patient_id>', methods=['GET', 'POST'])
@login_required
def edit_patient(patient_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    if request.method == 'POST':
        name = request.form['name']
        gender = request.form['gender']
        birth_date = request.form['birth_date']
        phone = request.form['phone']
        address = request.form['address']
        card_number = request.form.get('card_number', '')

        try:
            cursor.execute("""
                UPDATE 病人 
                SET 姓名=%s, 性别=%s, 出生日期=%s, 联系电话=%s, 住址=%s, 医保卡号=%s 
                WHERE 病人ID=%s
            """, (name, gender, birth_date, phone, address, card_number or None, patient_id))
            conn.commit()
            flash('病人信息更新成功！', 'success')
            return redirect(url_for('patients'))
        except Exception as e:
            conn.rollback()
            # flash('更新失败：' + str(e), 'danger')
            flash('更新失败：没有权限！', 'danger')
            return render_template('edit_patient.html', patient=request.form)

    # GET 请求，获取病人信息
    cursor.execute("SELECT * FROM 病人 WHERE 病人ID=%s", (patient_id,))
    patient = cursor.fetchone()
    cursor.close()
    conn.close()

    if patient is None:
        flash('病人不存在！', 'danger')
        return redirect(url_for('patients'))

    return render_template('edit_patient.html', patient=patient)

@app.route('/patients/delete/<int:patient_id>', methods=['DELETE'])
@login_required
def delete_patient(patient_id):
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # 首先检查是否存在关联的处方
        cursor.execute("SELECT COUNT(*) as count FROM 处方 WHERE 病人ID=%s", (patient_id,))
        result = cursor.fetchone()
        if result['count'] > 0:
            return jsonify({'success': False, 'message': '该病人有关联的处方记录，无法删除！'})

        # 如果没有关联处方，则删除病人
        cursor.execute("DELETE FROM 病人 WHERE 病人ID=%s", (patient_id,))
        conn.commit()
        return jsonify({'success': True, 'message': '病人删除成功！'})
    except Exception as e:
        conn.rollback()
        return jsonify({'success': False, 'message': str(e)})
    finally:
        cursor.close()
        conn.close()

# 处方登记
@app.route('/prescriptions', methods=['GET', 'POST'])
@login_required
def prescriptions():
    conn = get_db_connection()
    cursor = conn.cursor()
    if request.method == 'POST':
        patient_id = request.form['patient_id']
        doctor_id = request.form['doctor_id']
        diagnosis = request.form['diagnosis']
        try:
            cursor.execute("INSERT INTO 处方(病人ID, 医生ID, 诊断结果) VALUES(%s, %s, %s)",
                        (patient_id, doctor_id, diagnosis))
        except Exception as e:
            flash('没有权限！', 'danger')
            return redirect(url_for('prescriptions'))
        conn.commit()
        return redirect(url_for('prescriptions'))
    try:
        cursor.execute("SELECT 处方ID, 处方_病人.姓名 as 病人姓名, 处方_医生.姓名 as 医生姓名, 诊断结果, 开具时间 FROM 处方 JOIN 处方_病人 ON 处方.病人ID=处方_病人.病人ID JOIN 处方_医生 ON 处方.医生ID=处方_医生.医生ID ORDER BY 开具时间 DESC")

        prescriptions = cursor.fetchall()
        cursor.execute("SELECT 病人ID, 姓名 FROM 处方_病人")
        patients = cursor.fetchall()
        cursor.execute("SELECT 医生ID, 姓名, 科室名称 FROM 处方_医生")
        doctors = cursor.fetchall()
    except Exception as e:
        flash('没有权限！', 'danger')
        return redirect(url_for('index'))
    cursor.close()
    conn.close()
    return render_template('prescriptions.html', prescriptions=prescriptions, patients=patients, doctors=doctors)


# 处方明细添加
@app.route('/prescription/<int:prescription_id>/details', methods=['GET', 'POST'])
@login_required
def prescription_details(prescription_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    if request.method == 'POST':
        medicine_id = request.form['medicine_id']
        quantity = request.form['quantity']
        usage = request.form['usage']
        try:
            cursor.execute("INSERT INTO 处方明细(处方ID, 药品ID, 数量, 用法用量) VALUES(%s, %s, %s, %s)",
                       (prescription_id, medicine_id, quantity, usage))
        except Exception as e:
            flash('没有权限！', 'danger')
            return redirect(url_for('index'))
        conn.commit()
        return redirect(url_for('prescription_details', prescription_id=prescription_id))
    try:
        cursor.execute("SELECT m.明细ID, y.药品名称, m.数量, m.用法用量 FROM 处方明细 m JOIN 药品信息 y ON m.药品ID=y.药品ID WHERE m.处方ID=%s", (prescription_id,))
        details = cursor.fetchall()
        cursor.execute("SELECT 药品ID, 药品名称 FROM 药品信息")
        medicines = cursor.fetchall()
        cursor.execute("SELECT 处方ID, 处方_病人.姓名 AS 病人, 处方_医生.姓名 AS 医生, 开具时间, 诊断结果 FROM 处方 JOIN 处方_病人 ON 处方.病人ID=处方_病人.病人ID JOIN 处方_医生 ON 处方.医生ID=处方_医生.医生ID WHERE 处方ID=%s", (prescription_id,))
        prescription_info = cursor.fetchone()
    except Exception as e:
        flash('没有权限！', 'danger')
        return redirect(url_for('index'))
    cursor.close()
    conn.close()
    return render_template('prescription_details.html', details=details, medicines=medicines, prescription=prescription_info)

# 收费管理
@app.route('/billing', methods=['GET', 'POST'])
@login_required
def billing():
    conn = get_db_connection()
    cursor = conn.cursor()
    if request.method == 'POST':
        prescription_id = request.form['prescription_id']

        cashier = session.get('username')
        date = request.form['datetime']
        payment_method = request.form['payment_method']
        cursor.execute("SELECT * FROM 未缴费处方 WHERE 处方ID=%s",(prescription_id,))
        amount = cursor.fetchone()['待缴费金额']
        cursor.execute("INSERT INTO 收费记录(处方ID, 收费金额, 收费时间, 收费员, 支付方式) VALUES(%s, %s, %s, %s, %s)",
                       (prescription_id, amount, date, cashier, payment_method))
        conn.commit()
        return redirect(url_for('billing'))
    try:
        cursor.execute("SELECT 收费ID, 处方ID, 收费金额, 收费时间, 收费员, 支付方式, 病人姓名 FROM 收费记录_收费")
        bills = cursor.fetchall()
        cursor.execute("SELECT 处方ID, 病人姓名, 医生姓名, 开具时间, 诊断结果 FROM 收费记录_处方")
        prescriptions_list = cursor.fetchall()
        cursor.execute("SELECT * FROM 未缴费处方视图")
        unpaid_pres = cursor.fetchall()
    except Exception as e:
        flash('没有权限！', 'danger')
        return redirect(url_for('index'))
    cursor.close()
    conn.close()
    return render_template('billing.html', bills=bills, prescriptions=prescriptions_list, unpaid_pres=unpaid_pres)

# 药品入库 （自动更新库存由触发器完成）
@app.route('/stock_in', methods=['GET', 'POST'])
@login_required
def stock_in():
    conn = get_db_connection()
    cursor = conn.cursor()
    if request.method == 'POST':
        medicine_id = request.form['medicine_id']
        quantity = request.form['quantity']
        date = request.form['datetime']
        operator = session.get('username')
        supplier = request.form['supplier']
        cursor.execute("INSERT INTO 入库记录(药品ID, 数量, 入库时间, 操作员, 供应商) VALUES(%s, %s, %s, %s, %s)",
                       (medicine_id, quantity, date, operator, supplier))
        conn.commit()
        return redirect(url_for('stock_in'))
    try:
        cursor.execute("SELECT s.入库ID, m.药品名称, s.数量, s.入库时间, s.操作员, s.供应商 FROM 入库记录 s JOIN 药品信息 m ON s.药品ID=m.药品ID ORDER BY s.入库时间 DESC")
    except Exception as e:
        flash('没有权限！', 'danger')
        return redirect(url_for('index'))
    stock_ins = cursor.fetchall()
    cursor.execute("SELECT 药品ID, 药品名称 FROM 药品信息")
    medicines = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('stock_in.html', stock_ins=stock_ins, medicines=medicines)

# 药品出库 （自动更新库存由触发器完成）
@app.route('/stock_out', methods=['GET', 'POST'])
@login_required
def stock_out():
    conn = get_db_connection()
    cursor = conn.cursor()
    if request.method == 'POST':
        medicine_id = request.form['medicine_id']
        quantity = request.form['quantity']
        date = request.form['datetime']
        operator = session.get('username')
        departments = request.form['departments']
        try:
            cursor.execute("INSERT INTO 出库记录(药品ID, 数量, 出库时间, 操作员, 领用科室) VALUES(%s, %s, %s, %s, %s)",
                           (medicine_id, quantity, date, operator, departments))
            conn.commit()
        except Exception as e:
            conn.rollback()
            error_message = '出库数量超过库存数量'
            flash('<span class="error-message">出库数量超过库存数量</span>')
        return redirect(url_for('stock_out'))
    try:
        cursor.execute("SELECT s.出库ID, m.药品名称, s.数量, s.出库时间, s.操作员, s.领用科室 FROM 出库记录 s JOIN 药品信息 m ON s.药品ID=m.药品ID ORDER BY s.出库时间 DESC")

        stock_outs = cursor.fetchall()
        cursor.execute("SELECT 药品ID, 药品名称 FROM 药品信息")
        medicines = cursor.fetchall()
        cursor.execute("SELECT 科室ID, 科室名称 FROM 出库_科室")
        departments = cursor.fetchall()
    except Exception as e:
        flash('没有权限！', 'danger')
        return redirect(url_for('index'))
    cursor.close()
    conn.close()
    return render_template('stock_out.html', stock_outs=stock_outs, medicines=medicines, departments=departments)



# 数据备份（导出 SQL 文件）
# 数据备份（导出 SQL 文件）
@app.route('/backup')
@login_required
def backup():
    try:
        # 生成备份文件名（包含时间戳）
        from datetime import datetime
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_file = os.path.join(BACKUP_DIR, f'backup_{timestamp}.sql')

        # 使用 mysqldump 导出数据库
        cmd = [
            'mysqldump',
            f'--host={DB_CONFIG["host"]}',
            f'--port={DB_CONFIG["port"]}',
            f'--user={DB_CONFIG["user"]}',
            f'--password={DB_CONFIG["password"]}',
            '--no-create-db',  # 不包含 CREATE DATABASE 语句
            #'--skip-add-drop-table',  # 不包含 DROP TABLE 语句
            '--replace',  # 使用 REPLACE INTO 替代 INSERT INTO，避免主键冲突
            DB_CONFIG['db'],
            f'--result-file={backup_file}'
        ]
        subprocess.run(cmd, check=True)

        # 提供文件下载
        return send_file(backup_file, as_attachment=True, download_name=f'backup_{timestamp}.sql')
    except subprocess.CalledProcessError as e:
        # flash(f'备份失败：{str(e)}', 'danger')
        flash(f'备份失败：无权备份！', 'danger')
        return redirect(url_for('index'))
    except Exception as e:
        flash(f'发生错误：{str(e)}', 'danger')
        return redirect(url_for('index'))

# 数据恢复提示
# 数据恢复（从上传的 SQL 文件恢复）
@app.route('/restore', methods=['GET', 'POST'])
@login_required
def restore():
    if request.method == 'POST':
        # 检查是否有文件上传
        if 'file' not in request.files:
            flash('未选择文件', 'danger')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('未选择文件', 'danger')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            try:
                # 保存上传的文件
                filename = secure_filename(file.filename)
                upload_path = os.path.abspath(os.path.join(BACKUP_DIR, filename))  # 使用绝对路径
                file.save(upload_path)

                # 调试：检查文件是否存在
                if not os.path.exists(upload_path):
                    flash(f'文件 {upload_path} 不存在', 'danger')
                    return redirect(request.url)

                # 使用 mysql 命令恢复数据库，添加 --force 选项
                cmd = [
                    'mysql',
                    f'--host={DB_CONFIG["host"]}',
                    f'--port={DB_CONFIG["port"]}',
                    f'--user={DB_CONFIG["user"]}',
                    f'--password={DB_CONFIG["password"]}',
                    '--force',  # 忽略错误继续执行
                    DB_CONFIG['db'],
                    '-e', f'source {upload_path}'  # 正确包裹路径，避免多余引号
                ]
                result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=3600)
                if result.returncode != 0:
                    # logging.error(f'Restore failed: {result.stderr}')
                    flash(f'恢复失败：{result.stderr}', 'danger')
                    return redirect(url_for('index'))

                flash('数据库恢复成功', 'success')
                return redirect(url_for('index'))
            except subprocess.TimeoutExpired as e:
                # logging.error(f'Restore timed out: {str(e)}')
                flash('恢复超时，请检查文件大小或服务器状态', 'danger')
                return redirect(url_for('index'))
            except subprocess.CalledProcessError as e:
                # logging.error(f'Restore failed: {str(e)}')
                flash(f'恢复失败：{str(e)}', 'danger')
                return redirect(url_for('index'))
            except Exception as e:
                # logging.error(f'Error occurred: {str(e)}')
                flash(f'发生错误：{str(e)}', 'danger')
                return redirect(url_for('index'))
        else:
            flash('只允许上传 .sql 文件', 'danger')
            return redirect(request.url)
    return render_template('restore.html')

if __name__ == '__main__':
    app.run(debug=True)



# 其他模板可参照以上风格，根据路由传入的数据进行渲染。
