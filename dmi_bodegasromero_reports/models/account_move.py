from odoo import models, fields, api, _
from datetime import datetime
import base64
import xlsxwriter
from io import BytesIO


class AccountMove(models.Model):
    _inherit = "account.move"

    def action_export_account_xls(self):
        """
        Exporta las facturas seleccionadas en formato XLS con desglose por cabecera y líneas.
        """
        active_ids = self.env.context.get('active_ids', [])
        invoices = self.browse(active_ids)

        if not invoices:
            return

        buffer = BytesIO()
        workbook = xlsxwriter.Workbook(buffer)
        worksheet = workbook.add_worksheet("Desglose Facturas")

        bold = workbook.add_format({'bold': True})
        money_format = workbook.add_format({'num_format': '#,##0.00'})
        date_format = workbook.add_format({'num_format': 'dd/mm/yyyy'})
        # Establecer anchos mínimos para columnas
        worksheet.set_column('A:A', 16)  # Columna A (Cantidad o Factura N°)
        worksheet.set_column('B:B', 30)  # Columna B (Producto o Cliente o Dirección)
        worksheet.set_column('C:C', 20)  # Columna C (Cliente, Dirección, Total)
        worksheet.set_column('D:D', 30)  # Columna D
        worksheet.set_column('E:E', 15)  # Columna E
        worksheet.set_column('F:F', 20)  # Columna F (Fecha)

        row = 0
        grand_total = 0.0

        worksheet.write(row, 0, "Factura N°:", bold)
        worksheet.write(row, 1, "Cliente:", bold)
        worksheet.write(row, 2, "Fecha:", bold)
        worksheet.write(row, 3, "Dirección:", bold)
        worksheet.write(row, 4, "Total:", bold)
        row += 1

        for invoice in invoices:
            # Cabecera de factura
            worksheet.write(row, 0, invoice.name or '', bold)
            worksheet.write(row, 1, invoice.partner_id.name or '')
            worksheet.write(row, 2, invoice.invoice_date, date_format)
            address = f"{invoice.partner_id.state_id.name or ''}, {invoice.partner_id.city or ''}, {invoice.partner_id.country_id.name or ''}"
            worksheet.write(row, 3, address)
            worksheet.write(row, 4, invoice.amount_total, money_format)
            grand_total += invoice.amount_total
            row += 1

            # # Encabezados de líneas
            # worksheet.write(row, 2, "Producto", bold)
            # worksheet.write(row, 3, "Cantidad", bold)
            # worksheet.write(row, 4, "Importe", bold)
            # row += 1

            for line in invoice.invoice_line_ids:
                worksheet.write(row, 2, line.product_id.name or line.name)
                worksheet.write(row, 3, line.quantity)
                worksheet.write(row, 4, line.price_total, money_format)
                row += 1

            row += 2  # espacio entre facturas

        # Gran total al final del Excel
        worksheet.write(row, 3, "Total Facturación:", bold)
        worksheet.write(row, 4, grand_total, money_format)

        workbook.close()
        buffer.seek(0)
        file_data = buffer.read()
        filename = 'informe_facturacion_%s.xlsx' % datetime.now().strftime("%d-%m-%Y")

        attachment = self.env['ir.attachment'].create({
            'name': filename,
            'type': 'binary',
            'datas': base64.b64encode(file_data),
            'res_model': self._name,
            'res_id': self[0].id or invoices[0].id,
            'mimetype': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        })

        return {
            'type': 'ir.actions.act_url',
            'url': '/web/content/%s?download=true' % attachment.id,
            'target': 'new',
        }
