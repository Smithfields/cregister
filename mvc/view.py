from flask import Blueprint, render_template, send_file, request, jsonify, flash
from dicttoxml import dicttoxml # used to parse dictionary for REST XML rendering

from src.wrapper import *

from conf import config as cfg, utilities as util
from mvc import controller as ctrl

import re
from html import escape as htescape

logging.getLogger('dicttoxml').setLevel(logging.ERROR) # silencing 'dicttoxml' which generates a vast amount of INFO log
simple_page = Blueprint('simple_page', __name__, template_folder='templates')



@simple_page.route('/employee/look', methods=['GET', 'POST'])
def view_employee_form():
    if request.method == 'POST':  # this block is only entered when the form is submitted
        id = util.validate_int(request.form['id']) # input check
        if id is None:  # reset page with flash message if check fails
            flash(cfg.ERROR_MSG_PARAM) # not used in this app
            return cfg.ERROR_MSG_PARAM + cfg.FORM_EMPL_VIEW

        e = ctrl.find_employee(id)

        if e:
            return jsonify(e.__dict__()), 200,  cfg.HEADER_JSON
        else: # DB returned nothing and e is set to 'False'
            return cfg.ERROR_MSG_DB + ' > ' + htescape(str(id)) + cfg.FORM_EMPL_VIEW

    return cfg.FORM_EMPL_VIEW


@simple_page.route('/employee/all', methods=['GET'])
def view_all_employee():
    """
    can return json or xml
    :return:
    """
    e_all = ctrl.find_all_employee()
    if request.args.get('xml'):
        return dicttoxml(e_all, custom_root='employee_list', attr_type=False), 200, cfg.HEADER_XML
    else:
        return jsonify(e_all), 200, cfg.HEADER_JSON


@simple_page.route('/employee/add', methods=['GET', 'POST']) # Should be POST only in True REST
def view_add_employee():
    if request.method == 'POST':
        e = ctrl.add_employee(request.form)
        if not e:
            flash(cfg.ERROR_MSG_PARAM)
            return cfg.ERROR_MSG_PARAM + cfg.FORM_EMPL_ADD

        return jsonify(e.__dict__()), 200, cfg.HEADER_JSON

    return cfg.FORM_EMPL_ADD


@simple_page.route('/employee/edit/<id>', methods=['GET', 'POST'])  # Should be PUT only in True REST
def view_update_employee(id): # Should be PUT in True REST
    id = util.validate_int(id)  # input check
    if id is None:  # reset page with flash message if check fails
        return cfg.ERROR_MSG_PARAM

    if request.method == 'POST':
        #TODO: maintain Employee 'alive between both request', so no second fetch

        e = ctrl.update_employee(id, request.form)

        if not e:
            flash(cfg.ERROR_MSG_PARAM)
            return cfg.ERROR_MSG_PARAM + cfg.FORM_EMPL_ADD

        return jsonify(e.__dict__()), 200, cfg.HEADER_JSON

    e = ctrl.find_employee(id)

    if e:
        return render_template('empl_edit.html', id=int(e.id), f_name=e.f_name, l_name=e.l_name, email=e.email)
    else:
        return cfg.ERROR_MSG_DB

@simple_page.route('/menu/look', methods=['GET', 'POST'])
def view_menu():
    if request.method == 'POST':  #this block is only entered when the form is submitted
        id = util.validate_int(request.form['id']) #input check
        if id is None:  #reset page with flash message if check fails
            flash(cfg.ERROR_MSG_PARAM)
            return cfg.ERROR_MSG_PARAM + cfg.FORM_MENU_VIEW

        m = ctrl.find_menu(id)

        if m:
            return jsonify(m.__dict__()), 200, cfg.HEADER_JSON
        else:
            return cfg.ERROR_MSG_DB + ' > ' + htescape(str(id)) + cfg.FORM_MENU_VIEW

    return cfg.FORM_MENU_VIEW


@simple_page.route('/menu/all', methods=['GET'])
def view_all_menu():
    """
    can return json or xml
    :return:
    """
    m_all = ctrl.find_all_menu()

    if request.args.get('xml'):
        return dicttoxml(m_all, custom_root='menu_list', attr_type=False), 200, cfg.HEADER_XML
    else:
        return jsonify(m_all), 200, cfg.HEADER_JSON


@simple_page.route('/menu/add', methods=['GET', 'POST']) # Should be POST only in True REST
def view_add_menu():
    if request.method == 'POST':
        m = ctrl.add_menu(request.form)

        if not m:
            flash(cfg.ERROR_MSG_PARAM)
            return cfg.ERROR_MSG_PARAM + cfg.FORM_MENU_ADD

        return jsonify(m.__dict__()), 200, cfg.HEADER_JSON

    return cfg.FORM_MENU_ADD


@simple_page.route('/menu/edit/<id>', methods=['GET', 'POST']) # Should be PUT only in True REST
def view_update_menu(id):
    id = util.validate_int(id)  # input check
    if id is None:  # reset page with flash message if check fails
        return cfg.ERROR_MSG_PARAM

    if request.method == 'POST':
        #TODO: maintain Employee 'alive between both request', so no second fetch

        m = ctrl.update_menu(id, request.form)

        if not m:
            flash(cfg.ERROR_MSG_PARAM)
            return cfg.ERROR_MSG_PARAM

        return jsonify(m.__dict__()), 200, cfg.HEADER_JSON

    m = ctrl.find_menu(id)

    if m:
        return render_template('menu_edit.html', id=m.id, descr=m.descr, price=m.price)
    else:
        return cfg.ERROR_MSG_DB


@simple_page.route('/purchase/<id>', methods=['GET', 'POST'])
def view_one_purchase(id):
    id = util.validate_int(id)  # input check
    if id is None:  # reset page with flash message if check fails
        flash(cfg.ERROR_MSG_PARAM)  # not used in this app
        return cfg.ERROR_MSG_PARAM + cfg.FORM_EMPL_VIEW

    p = ctrl.find_purchase(id)

    if p:
        if request.args.get('xml'):
            return dicttoxml(p.__dict__(), custom_root='purchase', attr_type=False), 200, cfg.HEADER_XML
        else:
            return jsonify(p.__dict__()), 200, cfg.HEADER_JSON
    else:  # DB returned nothing and e is set to 'False'
        return cfg.ERROR_MSG_DB + ' > ' + htescape(str(id)) + cfg.FORM_EMPL_VIEW


@simple_page.route('/purchase/add', methods=['GET', 'POST'])
def view_do_purchase():
    if request.method == 'POST':
        empl_id = util.validate_int(request.form['empl_id'])  # input check
        menu_id_list_str = util.validate_string(request.form['menu_id_list'])

        if (empl_id is None) or (menu_id_list_str is None):  # reset page with flash message if check fails
            return cfg.ERROR_MSG_PARAM + cfg.FORM_PURCH_ADD

        e = ctrl.find_employee(empl_id)
        if not e:
            return cfg.ERROR_MSG_DB + ' > ' + htescape(str(empl_id)) + cfg.FORM_PURCH_ADD

        p = ctrl.initiate_purchase()
        p.employee = e

        # Each IDs must be tested as one unit (is it a valid int + exists in DB)
        # will interrupt function at next check in case there are not enough valid IDs
        menu_id_list_raw = re.compile(",").split(menu_id_list_str) # parses ids, seeks for comas
        for menu_id in menu_id_list_raw:
            r = util.validate_int(menu_id)
            if r is not None:
                m = ctrl.find_menu(r)
                if m:
                    p.addmenu(m)

        # if test yielded valid menus
        if len(p.menu_list) < 1: # parse failure
            return cfg.ERROR_MSG_PARAM + cfg.FORM_PURCH_ADD

        p = ctrl.do_total_purchase(p, e)
        return jsonify(p.__dict__()), 200, cfg.HEADER_JSON

    return cfg.FORM_PURCH_ADD


@simple_page.route('/receipt/<id>')
def view_get_receipt(id):
    id = util.validate_int(id)  # input check
    if id is None:  # reset page with flash message if check fails
        return cfg.ERROR_MSG_PARAM

    data_list = ctrl.prepare_receipt_data(id)
    if not data_list:
        return cfg.ERROR_MSG_DB + ' > ' + htescape(str(id))

    file_buffer = ctrl.make_receipt_pdf(data_list)

    filename = cfg.DFLT_FILENAME.format(id)
    return send_file(file_buffer, as_attachment=True, attachment_filename=filename, mimetype=cfg.SENDFILE_PDF)
