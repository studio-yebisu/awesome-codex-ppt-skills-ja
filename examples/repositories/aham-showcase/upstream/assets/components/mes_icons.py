# -*- coding: utf-8 -*-
"""MES 主题具象矢量图库（24x24 基准，Aham 极简线性风：单色描边 + ACC 点缀）"""
ACC = "#336EE8"

def _w(cx, cy, size, inner, color, sw=1.7):
    sc = size/24.0
    return (f'<g transform="translate({cx-size/2:.2f},{cy-size/2:.2f}) scale({sc:.4f})" '
            f'fill="none" stroke="{color}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round">{inner}</g>')

def worker(cx, cy, s=40, c="#6E6E6E"):
    return _w(cx, cy, s, '<circle cx="12" cy="7" r="3.2"/><path d="M5.5 20.5 v-1 a6.5 6.5 0 0 1 13 0 v1"/>', c)

def machine(cx, cy, s=40, c="#6E6E6E"):
    i = ('<rect x="3" y="9" width="18" height="11" rx="1.5"/><rect x="8" y="5" width="8" height="4" rx="1"/>'
         '<rect x="6" y="12" width="6" height="5" rx="0.8"/>'
         f'<circle cx="16" cy="13.5" r="1" fill="{ACC}" stroke="none"/><circle cx="16" cy="16.5" r="1"/>'
         '<path d="M6 20 v1.6 M18 20 v1.6"/>')
    return _w(cx, cy, s, i, c)

def warehouse(cx, cy, s=40, c="#6E6E6E"):
    i = ('<path d="M2.5 10 L12 4 L21.5 10"/><path d="M5 10 V20 H19 V10"/>'
         '<rect x="9.5" y="13" width="5" height="7"/><path d="M5.5 13 H8 M16 13 H18.5"/>')
    return _w(cx, cy, s, i, c)

def shelf(cx, cy, s=40, c="#6E6E6E"):
    i = ('<rect x="3.5" y="4" width="17" height="16" rx="1"/><path d="M3.5 11.5 H20.5"/>'
         f'<rect x="5.5" y="6.2" width="5" height="3.8"/><rect x="13" y="13.2" width="5" height="4.6" fill="{ACC}" fill-opacity="0.12"/>'
         '<path d="M5.5 20 v2 M18.5 20 v2"/>')
    return _w(cx, cy, s, i, c)

def conveyor(cx, cy, s=40, c="#6E6E6E"):
    i = ('<circle cx="5.5" cy="16" r="3"/><circle cx="18.5" cy="16" r="3"/>'
         '<path d="M5.5 13 H18.5 M5.5 19 H18.5"/>'
         f'<rect x="9" y="7" width="6" height="4" rx="0.6" fill="{ACC}" fill-opacity="0.12"/>'
         '<path d="M10.5 16 h3 m-1.2 -1.4 l1.4 1.4 l-1.4 1.4"/>')
    return _w(cx, cy, s, i, c)

def andon(cx, cy, s=40, c="#6E6E6E"):
    i = ('<path d="M9 8.2 a3 3 0 0 1 6 0"/><rect x="9" y="8" width="6" height="10" rx="0.6"/>'
         f'<rect x="9" y="8" width="6" height="3.3" fill="{ACC}" stroke="none"/><path d="M9 8.2 a3 3 0 0 1 6 0 V8"/>'
         '<path d="M9 11.3 H15 M9 14.6 H15"/><path d="M7.5 18 H16.5 M12 18 V21 M9 21 H15"/>'
         f'<path d="M17 8.5 a4 4 0 0 1 0 7" stroke="{ACC}"/><path d="M19.4 6.5 a7.5 7.5 0 0 1 0 11" stroke="{ACC}"/>')
    return _w(cx, cy, s, i, c)

def scanner(cx, cy, s=40, c="#6E6E6E"):
    i = ('<rect x="4" y="6" width="16" height="11" rx="1"/>'
         '<path d="M7 9 V14 M10 9 V14 M13 9 V14 M16.5 9 V14"/>'
         f'<path d="M3 11.5 H21" stroke="{ACC}"/>')
    return _w(cx, cy, s, i, c)

def screen(cx, cy, s=40, c="#6E6E6E"):
    i = ('<rect x="3" y="4" width="18" height="13" rx="1.5"/><path d="M9 17 V20 H15 V17 M7 20 H17"/>'
         f'<path d="M7 14 V11 M10.5 14 V8 M14 14 V12 M17.5 14 V9.5" stroke="{ACC}"/>')
    return _w(cx, cy, s, i, c)

def sensor(cx, cy, s=40, c="#6E6E6E"):
    i = ('<rect x="8" y="11" width="8" height="8" rx="1.5"/><circle cx="12" cy="15" r="1.8"/>'
         '<path d="M12 11 V7"/><path d="M8.8 8 a4.5 4.5 0 0 1 6.4 0"/>'
         f'<circle cx="12" cy="5" r="1.3" fill="{ACC}" stroke="none"/>')
    return _w(cx, cy, s, i, c)

def motor(cx, cy, s=40, c="#6E6E6E"):
    i = ('<rect x="4" y="8" width="13" height="9" rx="1.5"/><path d="M17 12.5 H21"/>'
         '<path d="M6.5 8 V17 M9 8 V17 M11.5 8 V17"/><rect x="7" y="5" width="5" height="3" rx="0.5"/>'
         '<path d="M6 17 v2 M14 17 v2"/>')
    return _w(cx, cy, s, i, c)

def camera(cx, cy, s=40, c="#6E6E6E"):
    i = ('<rect x="3" y="7" width="18" height="11" rx="1.5"/><circle cx="12" cy="12.5" r="3.2"/>'
         '<circle cx="12" cy="12.5" r="1.2"/><path d="M8 7 V5 H13 V7"/>'
         f'<circle cx="6.5" cy="9.8" r="0.9" fill="{ACC}" stroke="none"/>')
    return _w(cx, cy, s, i, c)

def qrcode(cx, cy, s=40, c="#6E6E6E"):
    i = ('<rect x="3.5" y="3.5" width="17" height="17" rx="1.5"/>'
         '<rect x="6" y="6" width="4" height="4"/><rect x="14" y="6" width="4" height="4"/><rect x="6" y="14" width="4" height="4"/>'
         f'<rect x="14" y="14" width="1.8" height="1.8" fill="{ACC}" stroke="none"/><rect x="17" y="14" width="1.5" height="1.5" fill="{ACC}" stroke="none"/><rect x="14.5" y="17" width="1.5" height="1.5" fill="{ACC}" stroke="none"/>')
    return _w(cx, cy, s, i, c)

def bin(cx, cy, s=40, c="#6E6E6E"):
    i = ('<path d="M5 8 H19 L17.3 19 H6.7 Z"/><path d="M4 8 H20"/><path d="M9.5 11 H14.5"/>'
         f'<rect x="9" y="13" width="6" height="3" fill="{ACC}" fill-opacity="0.12"/>')
    return _w(cx, cy, s, i, c)

def gauge(cx, cy, s=40, c="#6E6E6E"):
    i = ('<path d="M4 17 A8 8 0 0 1 20 17"/><path d="M7 20 H17"/>'
         f'<path d="M12 17 L16 11.5" stroke="{ACC}"/><circle cx="12" cy="17" r="1.3" fill="{ACC}" stroke="none"/>'
         '<path d="M4 17 h1.5 M18.5 17 H20 M6 11.5 l1 1 M18 11.5 l-1 1"/>')
    return _w(cx, cy, s, i, c)

def badge(cx, cy, s=40, c="#6E6E6E"):
    i = ('<rect x="4" y="4" width="16" height="16" rx="2"/><circle cx="9" cy="10" r="2.3"/>'
         '<path d="M13.5 8 H17 M13.5 11 H17"/>'
         f'<path d="M6.5 15.8 L8.5 17.8 L12.5 13.8" stroke="{ACC}"/>')
    return _w(cx, cy, s, i, c)

def clock(cx, cy, s=40, c="#6E6E6E"):
    return _w(cx, cy, s, f'<circle cx="12" cy="12" r="8"/><path d="M12 7 V12 L15.5 14" stroke="{ACC}"/>', c)

def robotarm(cx, cy, s=40, c="#6E6E6E"):
    i = ('<path d="M8 21 H16 M10 21 V18 H14 V21"/><path d="M12 18 L7 12"/><circle cx="7" cy="12" r="1.4"/>'
         '<path d="M7 12 L13 8"/><circle cx="13" cy="8" r="1.2"/>'
         f'<path d="M13 8 L16.5 5.5 M15.5 4 L17.5 6 M16 7.5 L18 9.5" stroke="{ACC}"/>')
    return _w(cx, cy, s, i, c)

def agv(cx, cy, s=40, c="#6E6E6E"):
    i = ('<rect x="4" y="9" width="16" height="6" rx="1.5"/>'
         f'<rect x="8" y="4.5" width="8" height="4.5" rx="0.6" fill="{ACC}" fill-opacity="0.12"/>'
         '<circle cx="8" cy="17.5" r="2"/><circle cx="16" cy="17.5" r="2"/>'
         f'<path d="M20 12 h2.5" stroke="{ACC}"/>')
    return _w(cx, cy, s, i, c)

def inspect(cx, cy, s=40, c="#6E6E6E"):
    i = ('<circle cx="10" cy="10" r="6"/><path d="M14.5 14.5 L20 20"/>'
         f'<path d="M7.3 10 L9.3 12 L13 8.2" stroke="{ACC}"/>')
    return _w(cx, cy, s, i, c)

def gearmold(cx, cy, s=40, c="#6E6E6E"):
    # 模具：上下两半模 + 型腔 + 导柱
    i = ('<rect x="4" y="4.6" width="16" height="6.4" rx="1"/>'
         '<rect x="4" y="13" width="16" height="6.4" rx="1"/>'
         f'<rect x="9.3" y="8" width="5.4" height="3" fill="{ACC}" fill-opacity="0.18" stroke="none"/>'
         f'<rect x="9.3" y="13" width="5.4" height="3" fill="{ACC}" fill-opacity="0.18" stroke="none"/>'
         '<path d="M7 4.6 V2.6 M17 4.6 V2.6 M7 19.4 V21.4 M17 19.4 V21.4"/>')
    return _w(cx, cy, s, i, c)

def injection(cx, cy, s=40, c="#6E6E6E"):
    # 注塑机：机身 + 料斗 + 合模板 + 螺杆
    i = ('<rect x="3" y="10" width="11" height="8" rx="1"/>'
         f'<path d="M6 10 V7 h4 l-1 3" fill="{ACC}" fill-opacity="0.15"/>'
         '<path d="M14 13 H17 M17 9 V18 M17 13 H21 M21 9 V18"/>'
         '<path d="M5 18 v1.6 M12 18 v1.6"/>')
    return _w(cx, cy, s, i, c)

def alert(cx, cy, s=40, c="#6E6E6E"):
    i = (f'<path d="M12 4 L21 19 H3 Z"/><path d="M12 10 V14.5" stroke="{ACC}"/>'
         f'<circle cx="12" cy="16.8" r="0.7" fill="{ACC}" stroke="none"/>')
    return _w(cx, cy, s, i, c)

def doc(cx, cy, s=40, c="#6E6E6E"):
    i = ('<path d="M6 3 H14 L19 8 V21 H6 Z"/><path d="M14 3 V8 H19"/>'
         '<path d="M9 12 H16 M9 15 H16 M9 18 H13"/>')
    return _w(cx, cy, s, i, c)

def network(cx, cy, s=40, c="#6E6E6E"):
    i = (f'<circle cx="12" cy="12" r="2.4" fill="{ACC}" fill-opacity="0.12"/>'
         '<circle cx="5" cy="6" r="1.7"/><circle cx="19" cy="6" r="1.7"/><circle cx="5" cy="18" r="1.7"/><circle cx="19" cy="18" r="1.7"/>'
         '<path d="M10.3 10.6 L6.2 7.2 M13.7 10.6 L17.8 7.2 M10.3 13.4 L6.2 16.8 M13.7 13.4 L17.8 16.8"/>')
    return _w(cx, cy, s, i, c)

def database(cx, cy, s=40, c="#6E6E6E"):
    i = ('<ellipse cx="12" cy="6" rx="7" ry="2.6"/><path d="M5 6 V18 a7 2.6 0 0 0 14 0 V6"/>'
         '<path d="M5 12 a7 2.6 0 0 0 14 0"/>')
    return _w(cx, cy, s, i, c)

ALL = {"worker": worker, "machine": machine, "warehouse": warehouse, "shelf": shelf, "conveyor": conveyor,
       "andon": andon, "scanner": scanner, "screen": screen, "sensor": sensor, "motor": motor,
       "camera": camera, "qrcode": qrcode, "bin": bin, "gauge": gauge, "badge": badge, "clock": clock,
       "robotarm": robotarm, "agv": agv, "inspect": inspect, "gearmold": gearmold, "alert": alert,
       "doc": doc, "network": network, "database": database}
