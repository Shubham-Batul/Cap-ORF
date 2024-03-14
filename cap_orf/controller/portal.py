from odoo import http, _
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal, pager


class ORFPurchase(CustomerPortal):

    def _prepare_home_portal_values(self, counters):
        values = super(ORFPurchase, self)._prepare_home_portal_values(counters)
        if 'orf_count' in counters:
            values['orf_count'] = request.env['purchase.orf'].sudo().search_count([])
        return values

    @http.route(['/my/ORF_Purchase'], type='http', website=True)
    def portal_my_list_view(self, sortby=None, **kwargs):
        searchbar_sorting = {
            'id': {'label': _('ID'), 'order': 'id asc'},
            'name': {'label': _('Name'), 'order': 'name'},
        }
        if not sortby:
            sortby = 'id'

        orf_purchase_obj = request.env['purchase.orf']
        order = searchbar_sorting[sortby]['order']
        orf_purchase = orf_purchase_obj.search([], order=order)
        return request.render("cap_orf.portal_layout_orf_purchase", {
            'orf_purchase': orf_purchase,
            'page_name': 'list_view_orf_purchase',
            'searchbar_sorting': searchbar_sorting,
            'sortby': sortby
        })

    @http.route(['/my/ORF_Purchase/<model("purchase.orf"):orf_id>'], type='http', website=True)
    def portal_my_form_view(self, orf_id, **kwargs):
        vals = {"orf": orf_id, 'page_name': 'orf_purchase_form_view'}
        sub_records = request.env['purchase.orf'].search([])
        sub_ids = sub_records.ids
        sub_index = sub_ids.index(orf_id.id)
        if sub_index != 0 and sub_ids[sub_index - 1]:
            vals['prev_record'] = '/my/ORF_Purchase/{}'.format(sub_ids[sub_index - 1])
        if sub_index < len(sub_ids) - 1 and sub_ids[sub_index + 1]:
            vals['next_record'] = '/my/ORF_Purchase/{}'.format(sub_ids[sub_index + 1])
        return request.render("cap_orf.form_view_portal_orf_purchase", vals)
