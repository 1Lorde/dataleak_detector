from flask_table import Table, Col


class DeviceTable(Table):
    classes = ['table', 'is-striped', 'is-hoverable', 'is-fullwidth']
    id = Col("ID")
    name = Col('Name')
    serial = Col('Serial number')

    def get_tr_attrs(self, item):
        return {"onclick": 'window.location="/devices/' + str(item.id) + '/edit"'}
