# -*- coding: utf-8 -*-

"""
@Datetime: 2019/2/21
@Author: Zhang Yafei
"""
import datetime
import json, requests

from sqlalchemy import func

from application import db, app
from common.libs.helper import getCurrentDate
from common.libs.pay.WechatService import WechatService
from common.models.food.food import Food
from common.models.member.OauthMemberBind import OauthMemberBind
from common.models.pay.pay_order import PayOrder
from common.models.pay.pay_order_item import PayOrderItem
from common.models.queue.queue_list import QueueList
from common.models.food.food_sale_change_log import FoodSaleChangeLog

"""
python manage.py runjob -m queue/index
"""


class JobTask(object):
    def __init__(self):
        pass

    def run(self, *args, **kwargs):
        queue_list = QueueList.query.filter_by(status=-1).order_by(QueueList.id.asc()).limit(1).all()
        for item in queue_list:
            if item.queue_name == 'pay':
                pass
            item.status = 1
            item.updated_time = getCurrentDate()
            db.session.add(item)
            db.session.commit()

    def handle_pay(self, item):
        data = json.loads(item.data)
        if 'member_id' not in data or 'pay_order_id' not in data:
            return False
        oauth_bind_info = OauthMemberBind.query.filter_by(member_id=data['member_id']).first()
        if not oauth_bind_info:
            return False
        pay_order_info = PayOrder.query.filter_by(id=data['pay_order_id']).first()
        if not pay_order_info:
            return False
        pay_order_items = PayOrderItem.query.filter_by(pay_order_id=pay_order_info.id).all()
        notice_content = []
        # 更新销售数量
        if pay_order_items:
            date_from = datetime.datetime.now().strftime('%Y-%m-01 00:00:00')
            date_to = datetime.datetime.now().strftime('%Y-%m-31 23:59:59')
            for item in pay_order_items:
                tmp_food_info = Food.query.filter_by(id=item.food_id).first()
                if not tmp_food_info:
                    continue
                notice_content.append('{0} {1}份'.format(tmp_food_info.name, item.quantity))
                # 当月的销售
                tmp_stat_info = db.session.query(FoodSaleChangeLog, func.sum(FoodSaleChangeLog.quantity).label('total'))\
                    .filter(FoodSaleChangeLog.food_id == item.food_id)\
                    .filter(FoodSaleChangeLog.created_time >= date_from, FoodSaleChangeLog.created_time <= date_to).first()
                tmp_month_count = tmp_stat_info[1] if tmp_stat_info[1] else 0

                tmp_food_info.total_count += 1
                tmp_food_info.month_count = tmp_month_count
                db.session.add(tmp_food_info)
                db.session.commit()

        keyword1_val = str(pay_order_info.created_time)
        keyword2_val = str(pay_order_info.total_price)
        keyword3_val = '.'.join(notice_content)
        keyword4_val = str(pay_order_info.order_number)
        keyword5_val = ''  #
        keyword6_val = pay_order_info.note if pay_order_info.note else '无'

        target_wechat = WechatService()
        access_token = target_wechat.get_access_token()
        url = 'https://api.weixin.qq.com/cgi-bin/message/wxopen/template/send?access_token={0}'.format(access_token)
        params = {
            "touser": oauth_bind_info.openid,
            "template_id": "gpcSzzTotbJU5_0xdTQdjExMKD3JEGmckVjigkw4SB8",
            "page": "pages/my/order_list",
            "form_id": pay_order_info.prepay_id,
            "data": {
                "keyword1": {
                    "value": keyword1_val
                },
                "keyword2": {
                    "value": keyword2_val
                },
                "keyword3": {
                    "value": keyword3_val
                },
                "keyword4": {
                    "value": keyword4_val
                },
                "keyword5": {
                    "value": keyword5_val
                },
                "keyword6": {
                    "value": keyword6_val
                }
            },
        }
        headers = {'Content-Type': 'application/json'}
        r = requests.post(url=url, headers=headers, json=params)
        r.encoding = 'utf-8'
        app.logger.info(r.text)
        return True
