import streamlit as st
import pandas as pd
import streamlit.components.v1 as components
from datetime import datetime
import requests

# ========== TELEGRAM SETTINGS ==========
TELEGRAM_BOT_TOKEN = "8854223665:AAHR96ibnwbgH2V6vgLkCzTV8yy6zoDDq0U"
TELEGRAM_CHAT_ID = "6676779863"


def send_telegram_notification(order_data, notification_type="new_order"):
    try:
        if notification_type == "new_order":
            items_list = "\n".join([
                f"- {item['المنتج']}: {item['الكمية']} كجم = {item['المجموع']} ج.م"
                for item in order_data['items']
            ])

            total_products = order_data['total']
            delivery = order_data.get('delivery', 0)
            discount = order_data.get('discount', 0)
            final_total = total_products + delivery - discount

            discount_text = ""
            if discount > 0:
                discount_text = f"\n🎁 الخصم: {discount} ج.م"

            message = (
                f"🛒 طلب جديد واصل!\n\n"
                f"👤 العميل: {order_data['name']}\n"
                f"📱 الهاتف: {order_data['phone']}\n"
                f"📍 العنوان: {order_data['address']}\n"
                f"🌍 المنطقة: {order_data.get('zone', 'غير محدد')}\n\n"
                f"📦 المنتجات:\n{items_list}\n\n"
                f"💰 المنتجات: {total_products} ج.م\n"
                f"🚚 التوصيل: {delivery} ج.م{discount_text}\n"
                f"💵 الإجمالي النهائي: {final_total} ج.م"
            )

        elif notification_type == "delivered":
            total_products = order_data['total']
            delivery = order_data.get('delivery', 0)
            discount = order_data.get('discount', 0)
            final_total = total_products + delivery - discount

            message = (
                f"✅ تم تسليم الطلب!\n\n"
                f"👤 العميل: {order_data['name']}\n"
                f"📱 الهاتف: {order_data['phone']}\n"
                f"📅 وقت الطلب: {order_data['time']}\n"
                f"💵 المبلغ: {final_total} ج.م\n\n"
                f"🎉 شكراً لثقتكم في خير مصر!"
            )

        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        payload = {
            "chat_id": TELEGRAM_CHAT_ID,
            "text": message,
            "parse_mode": "Markdown"
        }

        response = requests.post(url, json=payload, timeout=5)
        return response.status_code == 200
    except Exception as e:
        st.error(f"فشل إرسال إشعار التلجرام: {e}")
        return False


# ========== PAGE CONFIG ==========
st.set_page_config(page_title="Khair Misr System", page_icon="🥗", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;700&display=swap');
    html, body, [class*="css"] { font-family: 'Cairo', sans-serif; background-color: #f8faf8; }
    .product-box { background-color: white; padding: 20px; border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); border: 1px solid #eef2ee; text-align: center; margin-bottom: 20px; min-height: 180px; }
    .product-box:hover { transform: translateY(-5px); box-shadow: 0 10px 15px rgba(0,0,0,0.1); }
    .metric-card { background: linear-gradient(135deg, #2e7d32 0%, #4caf50 100%); color: white; padding: 20px; border-radius: 12px; text-align: center; box-shadow: 0 4px 10px rgba(0,0,0,0.1); }
    .stButton>button { border-radius: 10px; font-weight: bold; background-color: #2e7d32; color: white; border: none; }
    .stepper { display: flex; justify-content: space-between; list-style: none; padding: 0; margin: 20px 0; }
    .step { flex: 1; text-align: center; padding: 10px; border-bottom: 4px solid #ddd; color: #999; font-size: 14px; }
    .step-active { border-bottom-color: #2e7d32; color: #2e7d32; font-weight: bold; }
    .delivery-box { background: linear-gradient(135deg, #ff9800 0%, #f57c00 100%); color: white; padding: 15px; border-radius: 12px; text-align: center; margin: 10px 0; }
    .discount-box { background: linear-gradient(135deg, #e91e63 0%, #c2185b 100%); color: white; padding: 15px; border-radius: 12px; text-align: center; margin: 10px 0; }
    .zone-box { background: linear-gradient(135deg, #2196f3 0%, #1976d2 100%); color: white; padding: 15px; border-radius: 12px; text-align: center; margin: 10px 0; }
    .final-box { background: linear-gradient(135deg, #2e7d32 0%, #1b5e20 100%); color: white; padding: 20px; border-radius: 12px; text-align: center; margin: 10px 0; font-size: 24px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)


# ========== PRODUCTS DATA ==========
original_products = [
    {"id": 2, "name": "بطاطس تحمير", "name_en": "Frying Potato", "price": 12.0, "stock": 150},
    {"id": 3, "name": "بصل أحمر", "name_en": "Red Onion", "price": 10.0, "stock": 120},
    {"id": 4, "name": "بصل أبيض", "name_en": "White Onion", "price": 12.0, "stock": 80},
    {"id": 5, "name": "خيار", "name_en": "Greenhouse Cucumber", "price": 14.0, "stock": 90},
    {"id": 6, "name": "جزر", "name_en": "Sweet Carrot", "price": 8.0, "stock": 70},
    {"id": 7, "name": "فلفل أخضر", "name_en": "Green Bell Pepper", "price": 16.0, "stock": 60},
    {"id": 8, "name": "فلفل ألوان", "name_en": "Colored Pepper", "price": 35.0, "stock": 40},
    {"id": 9, "name": "باذنجان ابيض", "name_en": "Eggplant", "price": 8.0, "stock": 85},
    {"id": 10, "name": "باذنجان اسود", "name_en": "Baby Eggplant", "price": 10.0, "stock": 50},
    {"id": 11, "name": "كوسة", "name_en": "Fresh Zucchini", "price": 15.0, "stock": 65},
    {"id": 12, "name": "بامية", "name_en": "Okra Zero", "price": 40.0, "stock": 30},
    {"id": 13, "name": "فاصوليا خضراء", "name_en": "Green Beans", "price": 20.0, "stock": 45},
    {"id": 14, "name": "ليمون اصفر", "name_en": "Lime", "price": 25.0, "stock": 40},
    {"id": 15, "name": "ثوم", "name_en": "Local Garlic", "price": 30.0, "stock": 50},
    {"id": 16, "name": "موز بلدي", "name_en": "Local Banana", "price": 15.0, "stock": 150},
    {"id": 17, "name": "تفاح أحمر مستورد", "name_en": "Imported Red Apple", "price": 45.0, "stock": 80},
    {"id": 18, "name": "تفاح أخضر", "name_en": "Green Apple", "price": 50.0, "stock": 60},
    {"id": 19, "name": "برتقال يوسفي", "name_en": "Juice Orange", "price": 10.0, "stock": 200},
    {"id": 20, "name": "برتقال أبو سرة", "name_en": "Navel Orange", "price": 12.0, "stock": 180},
    {"id": 21, "name": "فراولة", "name_en": "Fresh Strawberry", "price": 25.0, "stock": 70},
    {"id": 22, "name": "مانجو عويس", "name_en": "Awees Mango", "price": 60.0, "stock": 50},
    {"id": 23, "name": "مانجو زبدية", "name_en": "Zebdia Mango", "price": 35.0, "stock": 100},
    {"id": 24, "name": "جوافة", "name_en": "Guava", "price": 18.0, "stock": 90},
    {"id": 25, "name": "رمان", "name_en": "Sweet Pomegranate", "price": 15.0, "stock": 85},
    {"id": 26, "name": "بطيخ", "name_en": "Watermelon (Piece)", "price": 40.0, "stock": 30},
    {"id": 27, "name": "كانتالوب", "name_en": "Cantaloupe", "price": 15.0, "stock": 75},
    {"id": 28, "name": "عنب بناتي أحمر", "name_en": "Red Grapes", "price": 30.0, "stock": 65},
    {"id": 29, "name": "عنب بناتي أخضر", "name_en": "Green Grapes", "price": 25.0, "stock": 60},
    {"id": 30, "name": "خوخ", "name_en": "Local Peach", "price": 22.0, "stock": 55},
    {"id": 31, "name": "حزمة مشكلة", "name_en": "Mixed Greens", "price": 2.0, "stock": 500},
    {"id": 32, "name": "جرجير", "name_en": "Fresh Arugula", "price": 2.5, "stock": 200},
    {"id": 33, "name": "ملوخية خضراء", "name_en": "Green Molokhia", "price": 12.0, "stock": 40},
    {"id": 34, "name": "سبانخ بلدي", "name_en": "Local Spinach", "price": 15.0, "stock": 35},
    {"id": 35, "name": "خس كابوتشا", "name_en": "Iceberg Lettuce", "price": 7.0, "stock": 80}
]


# ========== SESSION STATE INIT ==========
if 'products' not in st.session_state:
    st.session_state.products = original_products.copy()

if 'orders' not in st.session_state:
    st.session_state.orders = []

if 'cart_version' not in st.session_state:
    st.session_state.cart_version = 0

if 'feedback' not in st.session_state:
    st.session_state.feedback = []

if 'delivery_fee' not in st.session_state:
    st.session_state.delivery_fee = 20.0

if 'delivery_zones' not in st.session_state:
    st.session_state.delivery_zones = {
        "مدينة نصر": 20.0,
        "مصر الجديدة": 25.0,
        "المعادي": 30.0,
        "الدقي": 25.0,
        "الزمالك": 30.0,
        "العباسية": 15.0,
        "التحرير": 20.0,
        "القاهرة الجديدة": 35.0,
        "6 أكتوبر": 40.0,
        "الشيخ زايد": 45.0,
    }

if 'discount_settings' not in st.session_state:
    st.session_state.discount_settings = {
        "enabled": True,
        "threshold": 200.0,
        "percentage": 10.0,
    }


# ========== HELPER FUNCTIONS ==========
def translate(ar, en):
    return ar if st.session_state.lang == "العربية" else en


def calculate_discount(total):
    settings = st.session_state.discount_settings
    if not settings["enabled"] or total < settings["threshold"]:
        return 0.0
    return round(total * (settings["percentage"] / 100), 2)


def get_zone_delivery(zone_name):
    return st.session_state.delivery_zones.get(zone_name, st.session_state.delivery_fee)


def generate_receipt_html(order, index):
    items_html = "".join([f"<tr><td style='padding:8px; border-bottom:1px solid #eee;'>{it['المنتج']}</td><td style='text-align:center;'>{it['الكمية']}</td><td style='text-align:left;'>{it['المجموع']} ج.م</td></tr>" for it in order['items']])
    total_products = order['total']
    delivery = order.get('delivery', 0)
    discount = order.get('discount', 0)
    final_total = total_products + delivery - discount

    delivery_html = ""
    if delivery > 0:
        delivery_html = f"""
        <div style="margin-top:8px; padding:8px; background:#fff3e0; border-radius:5px; text-align:center; color:#e65100; font-weight:bold;">
            🚚 خدمة التوصيل ({order.get('zone', 'غير محدد')}): {delivery} ج.م
        </div>
        """

    discount_html = ""
    if discount > 0:
        discount_html = f"""
        <div style="margin-top:8px; padding:8px; background:#fce4ec; border-radius:5px; text-align:center; color:#c2185b; font-weight:bold;">
            🎁 خصم ({st.session_state.discount_settings['percentage']}%): -{discount} ج.م
        </div>
        """

    return f"""
    <div id="print_area_{index}" style="font-family:'Cairo', Arial; direction:rtl; padding:20px; border:1px solid #ddd; border-radius:10px; width:280px; margin:auto; background:white; color: black;">
        <h2 style="text-align:center; color:#2e7d32; margin:0;">🍓🥬🍉🥕 اسواق خير مصرللفواكه والخضروات </h2>
        <hr><div style="font-size:13px;"><p><b>العميل:</b> {order['name']}</p><p><b>الهاتف:</b> {order['phone']}</p><p><b>العنوان:</b> {order['address']}</p><p><b>المنطقة:</b> {order.get('zone', 'غير محدد')}</p></div>
        <table style="width:100%; font-size:12px; margin-top:10px; border-collapse:collapse;"><tr style="background:#f4f4f4;"><th>الصنف</th><th>كمية</th><th>سعر</th></tr>{items_html}</table>
        <div style="margin-top:8px; padding:8px; background:#e8f5e9; border-radius:5px; text-align:center; color:#2e7d32; font-weight:bold;">
            💰 المنتجات: {total_products} ج.م
        </div>
        {delivery_html}
        {discount_html}
        <div style="margin-top:10px; border-top:2px solid #2e7d32; padding-top:10px; font-weight:bold; text-align:center; background:#2e7d32; color:white; border-radius:5px; font-size:18px;">
            الإجمالي النهائي: {final_total} ج.م
        </div>
        <button onclick="window.print()" style="width:100%; margin-top:10px; background:#2e7d32; color:white; border:none; padding:10px; border-radius:5px; cursor:pointer;">🖨️ طباعة</button>
    </div>
    <style> @media print {{ body * {{ visibility: hidden; }} #print_area_{index}, #print_area_{index} * {{ visibility: visible; }} #print_area_{index} {{ position: absolute; left: 0; top: 0; width: 100%; }} button {{ display: none !important; }} }} </style>
    """


# ========== SIDEBAR ==========
with st.sidebar:
    st.markdown("<h1 style='text-align: center; color: #2e7d32;'>🍓🥬🍉🥕 اسواق خير مصرللفواكه والخضروات</h1>", unsafe_allow_html=True)
    st.image("https://cdn-icons-png.flaticon.com/512/2329/2329865.png", use_column_width=True)
    st.divider()
    st.session_state.lang = st.radio("🌐 Language:", ["العربية", "English"], horizontal=True)

    menu_options = {
        "Store": translate("🛒 متجرنا", "🛒 Our Store"),
        "Track": translate("🛍️ مشترياتك", "🛍️ My Orders"),
        "Admin": translate("📊 الإدارة", "📊 Admin")
    }
    selection = st.radio(translate("الانتقال إلى:", "Navigate:"), list(menu_options.values()))

    st.divider()
    with st.expander(translate("⭐ تقييم البرنامج", "Rate us")):
        stars = st.select_slider("Rating", options=["1", "2", "3", "4", "5"], value="5")
        note = st.text_input("Feedback")
        if st.button("Send"):
            st.session_state.feedback.append({
                "date": datetime.now().strftime("%Y-%m-%d"),
                "stars": stars,
                "note": note
            })
            st.success("شكراً لك!")


# ========== STORE PAGE ==========
if selection == menu_options["Store"]:
    st.title(translate("🍓🥬🍉🥕 اسواق خير مصرللفواكه والخضروات", "🥬 Khair Misr Market"))
    search = st.text_input(translate("🔍 ابحث عن منتج...", "🔍 Search..."))

    filtered = [p for p in st.session_state.products if search.lower() in p['name'].lower() or search.lower() in p['name_en'].lower()]

    cart = {}
    cols = st.columns(4)
    for i, prod in enumerate(filtered):
        with cols[i % 4]:
            st.markdown(f"<div class='product-box'><h3>{prod['name'] if st.session_state.lang == 'العربية' else prod['name_en']}</h3><h4 style='color:#2e7d32;'>{prod['price']} ج.م</h4></div>", unsafe_allow_html=True)
            qty = st.number_input(f"كجم", 0.0, float(prod['stock']), 0.0, 0.5, key=f"q_{prod['id']}_{st.session_state.cart_version}")
            if qty > 0:
                cart[prod['id']] = {"name": prod['name'], "qty": qty, "price": prod['price']}

    if cart:
        st.divider()
        col_c1, col_c2 = st.columns([2, 1])
        with col_c1:
            c_name = st.text_input(translate("الاسم:", "Name:"))
            c_phone = st.text_input(translate("الهاتف:", "Phone:"))
            c_addr = st.text_input(translate("العنوان:", "Address:"))

            zones = list(st.session_state.delivery_zones.keys())
            selected_zone = st.selectbox(translate("🌍 منطقة التوصيل:", "🌍 Delivery Zone:"), zones)

        with col_c2:
            total_sum = sum(v['qty'] * v['price'] for v in cart.values())
            delivery = get_zone_delivery(selected_zone)
            discount = calculate_discount(total_sum)
            final_total = total_sum + delivery - discount

            st.metric(translate("المنتجات", "Products"), f"{total_sum} ج.م")
            st.markdown(f"<div class='zone-box'>🌍 {selected_zone}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='delivery-box'>🚚 {translate('التوصيل', 'Delivery')}: {delivery} ج.م</div>", unsafe_allow_html=True)

            if discount > 0:
                st.markdown(f"<div class='discount-box'>🎁 {translate('خصم', 'Discount')} ({st.session_state.discount_settings['percentage']}%): {discount} ج.م</div>", unsafe_allow_html=True)
                st.info(f"💡 {translate('وفرنا لك خصم لأن طلبك أكبر من', 'You saved because your order is over')} {st.session_state.discount_settings['threshold']} ج.م!")

            st.markdown(f"<div class='final-box'>💵 {translate('الإجمالي النهائي', 'Final Total')}: {final_total} ج.م</div>", unsafe_allow_html=True)

            if st.button(translate("✅ تأكيد الطلب", "✅ Order Now"), use_container_width=True):
                if c_name and c_phone and c_addr:
                    new_order = {
                        "time": datetime.now().strftime("%Y-%m-%d %H:%M"),
                        "name": c_name,
                        "phone": c_phone,
                        "address": c_addr,
                        "zone": selected_zone,
                        "items": [{"المنتج": v['name'], "الكمية": v['qty'], "المجموع": v['qty']*v['price']} for v in cart.values()],
                        "total": total_sum,
                        "delivery": delivery,
                        "discount": discount,
                        "done": False
                    }

                    telegram_sent = send_telegram_notification(new_order, "new_order")
                    if telegram_sent:
                        st.success("📨 تم إرسال إشعار التلجرام!")
                    else:
                        st.warning("⚠️ الطلب تم لكن فشل إرسال إشعار التلجرام")

                    st.session_state.orders.append(new_order)
                    st.session_state.cart_version += 1
                    st.success("تم الإرسال!")
                    st.rerun()


# ========== TRACK ORDERS PAGE ==========
elif selection == menu_options["Track"]:
    st.title(translate("🛍️ تتبع مشترياتك", "🛍️ My Orders"))
    search_p = st.text_input(translate("رقم الهاتف:", "Phone:"), placeholder="01XXXXXXXXX")
    if search_p:
        user_orders = [o for o in st.session_state.orders if o['phone'] == search_p]

        for i, o in enumerate(reversed(user_orders)):
            with st.container(border=True):
                st.write(f"📅 {o['time']}")
                status = "نعم" if o['done'] else "لا"
                s_active = "step-active" if status == 'نعم' else ""
                st.markdown(f"<ul class='stepper'><li class='step step-active'>✅ استلام</li><li class='step step-active'>⏳ تجهيز</li><li class='step {s_active}'>🚚 توصيل</li></ul>", unsafe_allow_html=True)

                delivery = o.get('delivery', 0)
                discount = o.get('discount', 0)
                final = o['total'] + delivery - discount

                col_info1, col_info2, col_info3 = st.columns(3)
                with col_info1:
                    st.metric("المنتجات", f"{o['total']} ج.م")
                with col_info2:
                    st.metric("التوصيل", f"{delivery} ج.م", delta=o.get('zone', ''))
                with col_info3:
                    st.metric("النهائي", f"{final} ج.م", delta=f"-{discount}" if discount > 0 else None)

                components.html(generate_receipt_html(o, i), height=550)


# ========== ADMIN PAGE ==========
else:
    pwd = st.sidebar.text_input("Password", type="password")
    if pwd == "10.20.30.40.10":
        st.title(translate("📊 لوحة التحكم", "📊 Admin Dashboard"))
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            translate("📥 الطلبات", "Orders"),
            translate("📦 المخزون", "Inventory"),
            translate("⭐ التقييمات", "Reviews"),
            translate("🚚 مناطق التوصيل", "Delivery Zones"),
            translate("🎁 إعدادات الخصم", "Discount Settings")
        ])

        with tab1:
            if st.session_state.orders:
                orders_display = []
                for o in st.session_state.orders:
                    order_copy = o.copy()
                    order_copy['الإجمالي النهائي'] = o['total'] + o.get('delivery', 0) - o.get('discount', 0)
                    orders_display.append(order_copy)

                df_orders = pd.DataFrame(orders_display)
                st.dataframe(df_orders)

                st.markdown("---")
                st.subheader("📦 تحديث حالة الطلب")
                order_idx = st.selectbox(
                    "اختر الطلب",
                    range(len(st.session_state.orders)),
                    format_func=lambda i: f"#{i+1} - {st.session_state.orders[i]['name']} - {st.session_state.orders[i]['phone']}"
                )

                col_btn1, col_btn2 = st.columns(2)
                with col_btn1:
                    if not st.session_state.orders[order_idx]['done']:
                        if st.button("✅ تم التسليم", use_container_width=True):
                            st.session_state.orders[order_idx]['done'] = True
                            send_telegram_notification(st.session_state.orders[order_idx], "delivered")
                            st.success("✅ تم تحديث الحالة وإرسال إشعار التسليم!")
                            st.rerun()
                with col_btn2:
                    if st.button("❌ حذف الطلب", use_container_width=True):
                        st.session_state.orders.pop(order_idx)
                        st.warning("تم حذف الطلب")
                        st.rerun()
            else:
                st.info("لا يوجد طلبات حالياً")

        with tab2:
            st.subheader("إدارة المخزون والأسعار")
            edited = st.data_editor(st.session_state.products, num_rows="dynamic", use_container_width=True)
            if st.button("💾 حفظ التغييرات"):
                st.session_state.products = edited
                st.success("تم حفظ التغييرات!")

        with tab3:
            if st.session_state.feedback:
                st.table(pd.DataFrame(st.session_state.feedback))
            else:
                st.info("لا يوجد تقييمات حالياً")

        with tab4:
            st.subheader("🚚 إدارة مناطق التوصيل")
            st.markdown("---")

            zones_df = pd.DataFrame([
                {"المنطقة": zone, "سعر التوصيل": price}
                for zone, price in st.session_state.delivery_zones.items()
            ])
            st.dataframe(zones_df, use_container_width=True)

            st.markdown("---")
            st.subheader("➕ إضافة / تعديل منطقة")

            col_z1, col_z2 = st.columns(2)
            with col_z1:
                zone_name = st.text_input("اسم المنطقة:")
            with col_z2:
                zone_price = st.number_input("سعر التوصيل (ج.م):", min_value=0.0, value=25.0, step=5.0)

            if st.button("💾 حفظ المنطقة", use_container_width=True):
                if zone_name:
                    st.session_state.delivery_zones[zone_name] = zone_price
                    st.success(f"✅ تم حفظ منطقة {zone_name} بسعر {zone_price} ج.م")
                    st.rerun()

            st.markdown("---")
            st.subheader("🗑️ حذف منطقة")
            zone_to_delete = st.selectbox("اختر منطقة للحذف:", list(st.session_state.delivery_zones.keys()))
            if st.button("❌ حذف المنطقة", use_container_width=True):
                del st.session_state.delivery_zones[zone_to_delete]
                st.warning(f"تم حذف منطقة {zone_to_delete}")
                st.rerun()

        with tab5:
            st.subheader("🎁 إعدادات الخصم")
            st.markdown("---")

            settings = st.session_state.discount_settings

            col_d1, col_d2, col_d3 = st.columns(3)
            with col_d1:
                enabled = st.toggle("تفعيل الخصم", value=settings["enabled"])
            with col_d2:
                threshold = st.number_input("الحد الأدنى (ج.م):", min_value=0.0, value=settings["threshold"], step=50.0)
            with col_d3:
                percentage = st.number_input("نسبة الخصم (%):", min_value=0.0, max_value=100.0, value=settings["percentage"], step=5.0)

            if st.button("💾 حفظ إعدادات الخصم", use_container_width=True):
                st.session_state.discount_settings = {
                    "enabled": enabled,
                    "threshold": threshold,
                    "percentage": percentage
                }
                st.success("✅ تم حفظ إعدادات الخصم!")
                st.rerun()

            st.markdown("---")
            current_settings = st.session_state.discount_settings
            example_discount = calculate_discount(300)
            st.info(
                f"الخصم الحالي: {'مفعل' if current_settings['enabled'] else 'معطل'} | "
                f"الحد الأدنى: {current_settings['threshold']} ج.م | "
                f"نسبة الخصم: {current_settings['percentage']}% | "
                f"مثال: طلب 300 ج.م = خصم {example_discount} ج.م"
            )
    else:
        st.info("أدخل كلمة المرور")