# -*- coding: utf-8 -*-
"""Lucide 风格线性图标库（自包含，通用）。供 B·现代专业档内容页使用。
取色一律传入 brand.md/tokens.css 的角色色，不在此写死品牌色。"""
MONO="'JetBrains Mono', Consolas, monospace"
_ICONS = {
 "clipboard": '<rect x="6" y="4" width="12" height="18" rx="2"/><rect x="9" y="2.5" width="6" height="3.4" rx="1"/><path d="M9 11h6M9 15h6"/>',
 "play":      '<circle cx="12" cy="12" r="9"/><path d="M10 8.5l6 3.5-6 3.5z" fill="currentColor" stroke="none"/>',
 "activity":  '<path d="M3 12h4l3-8 4 16 3-8h4"/>',
 "check":     '<circle cx="12" cy="12" r="9"/><path d="M8 12.2l2.6 2.6L16 9"/>',
 "shield":    '<path d="M12 3l7 3v5c0 4.5-3 7.5-7 9-4-1.5-7-4.5-7-9V6z"/><path d="M9 12l2 2 4-4"/>',
 "wrench":    '<path d="M15 7a4 4 0 0 1-5 5l-5 5 2 2 5-5a4 4 0 0 0 5-5l-2 2-2-2 2-2z"/>',
 "gear":      '<circle cx="12" cy="12" r="3.2"/><path d="M12 3v3M12 18v3M3 12h3M18 12h3M5.5 5.5l2 2M16.5 16.5l2 2M18.5 5.5l-2 2M7.5 16.5l-2 2"/>',
 "grid":      '<rect x="4" y="4" width="7" height="7" rx="1"/><rect x="13" y="4" width="7" height="7" rx="1"/><rect x="4" y="13" width="7" height="7" rx="1"/><rect x="13" y="13" width="7" height="7" rx="1"/>',
 "box":       '<path d="M12 3l8 4.5v9L12 21l-8-4.5v-9z"/><path d="M4 7.5l8 4.5 8-4.5M12 12v9"/>',
 "package":   '<path d="M12 3l8 4.5v9L12 21l-8-4.5v-9z"/><path d="M4 7.5l8 4.5 8-4.5M12 12v9M8 5.2l8 4.6"/>',
 "file":      '<path d="M7 3h7l5 5v13H7z"/><path d="M14 3v5h5M10 13h6M10 17h6"/>',
 "bell":      '<path d="M6 16V11a6 6 0 0 1 12 0v5l2 2H4z"/><path d="M10 20a2 2 0 0 0 4 0"/>',
 "monitor":   '<rect x="3" y="4" width="18" height="12" rx="2"/><path d="M9 20h6M12 16v4"/>',
 "dashboard": '<rect x="3" y="4" width="18" height="16" rx="2"/><path d="M7 15v-3M12 15V9M17 15v-5"/>',
 "message":   '<path d="M4 5h16v11H9l-4 4z" /><path d="M8 9h8M8 12h5"/>',
 "server":    '<rect x="4" y="4" width="16" height="6" rx="1.5"/><rect x="4" y="14" width="16" height="6" rx="1.5"/><circle cx="8" cy="7" r="0.8" fill="currentColor"/><circle cx="8" cy="17" r="0.8" fill="currentColor"/>',
 "wifi":      '<path d="M3 9a14 14 0 0 1 18 0M6 12.5a9 9 0 0 1 12 0M9 16a4 4 0 0 1 6 0"/><circle cx="12" cy="19" r="1.1" fill="currentColor" stroke="none"/>',
 "database":  '<ellipse cx="12" cy="6" rx="7" ry="3"/><path d="M5 6v12c0 1.6 3.1 3 7 3s7-1.4 7-3V6M5 12c0 1.6 3.1 3 7 3s7-1.4 7-3"/>',
 "user":      '<circle cx="12" cy="8" r="4"/><path d="M5 21a7 7 0 0 1 14 0"/>',
 "users":     '<circle cx="9" cy="8" r="3.2"/><path d="M3.5 20a5.5 5.5 0 0 1 11 0"/><path d="M16 5.2a3.2 3.2 0 0 1 0 6M17 20a5.5 5.5 0 0 0-3-5"/>',
 "factory":   '<path d="M3 21V10l6 4V10l6 4V6l3 1v14z"/><path d="M3 21h18"/>',
 "cpu":       '<rect x="6" y="6" width="12" height="12" rx="2"/><rect x="9.5" y="9.5" width="5" height="5" rx="1"/><path d="M9 3v3M15 3v3M9 18v3M15 18v3M3 9h3M3 15h3M18 9h3M18 15h3"/>',
 "building":  '<rect x="5" y="3" width="14" height="18" rx="1.5"/><path d="M9 7h2M13 7h2M9 11h2M13 11h2M9 15h2M13 15h2M10 21v-3h4v3"/>',
 "truck":     '<rect x="2" y="7" width="12" height="9" rx="1.5"/><path d="M14 10h4l3 3v3h-7z"/><circle cx="7" cy="18" r="2"/><circle cx="17.5" cy="18" r="2"/>',
 "phone":     '<rect x="7" y="3" width="10" height="18" rx="2.5"/><path d="M11 18h2"/>',
 "scan":      '<path d="M4 8V5a1 1 0 0 1 1-1h3M16 4h3a1 1 0 0 1 1 1v3M20 16v3a1 1 0 0 1-1 1h-3M8 20H5a1 1 0 0 1-1-1v-3"/><path d="M4 12h16"/>',
 "target":    '<circle cx="12" cy="12" r="8.5"/><circle cx="12" cy="12" r="4.8"/><circle cx="12" cy="12" r="1.4" fill="currentColor" stroke="none"/>',
 "flag":      '<path d="M6 21V4M6 4h11l-2.5 4L17 12H6"/>',
 "clock":     '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3.5 2"/>',
 "refresh":   '<path d="M20 11a8 8 0 0 0-14-4.5L4 8M4 4v4h4M4 13a8 8 0 0 0 14 4.5L20 16M20 20v-4h-4"/>',
 "trend":     '<path d="M3 17l6-6 4 4 8-8"/><path d="M15 7h6v6"/>',
 "layers":    '<path d="M12 3l9 5-9 5-9-5z"/><path d="M3 13l9 5 9-5M3 16.5l9 5 9-5" opacity="0.7"/>',
 "link":      '<path d="M9 12a4 4 0 0 1 4-4h2a4 4 0 0 1 0 8h-1"/><path d="M15 12a4 4 0 0 1-4 4H9a4 4 0 0 1 0-8h1"/>',
 "list":      '<path d="M8 6h12M8 12h12M8 18h12"/><circle cx="4" cy="6" r="1.2" fill="currentColor" stroke="none"/><circle cx="4" cy="12" r="1.2" fill="currentColor" stroke="none"/><circle cx="4" cy="18" r="1.2" fill="currentColor" stroke="none"/>',
 "map":       '<path d="M9 4L4 6v14l5-2 6 2 5-2V4l-5 2-6-2z"/><path d="M9 4v14M15 6v14"/>',
 "wallet":    '<rect x="3" y="6" width="18" height="13" rx="2"/><path d="M3 10h18M16 14h2"/>',
 "calendar":  '<rect x="4" y="5" width="16" height="16" rx="2"/><path d="M4 9h16M8 3v4M16 3v4"/>',
 "route":     '<circle cx="6" cy="19" r="2.4"/><circle cx="18" cy="6" r="2.4"/><path d="M8 17.5C14 16 16 14 16 9.5"/>',
 "bolt":      '<path d="M13 2L5 13h6l-2 9 9-12h-6z"/>',
 "search":    '<circle cx="11" cy="11" r="6.5"/><path d="M16 16l4.5 4.5"/>',
 "settings":  '<circle cx="12" cy="12" r="3"/><path d="M12 2v3M12 19v3M4.2 4.2l2.1 2.1M17.7 17.7l2.1 2.1M2 12h3M19 12h3M4.2 19.8l2.1-2.1M17.7 6.3l2.1-2.1"/>',
}

def ICON(name, x, y, size=24, color="#262626", sw=1.7):
    inner=_ICONS.get(name, _ICONS["box"]); s=size/24.0
    return (f'<g transform="translate({x},{y}) scale({s})" fill="none" stroke="{color}" '
            f'stroke-width="{sw/s if s else sw}" stroke-linecap="round" stroke-linejoin="round">{inner}</g>')

def icon_circle(name, cx, cy, r=18, color="#262626", bg="#F3F3F3", ring=None, isize=None):
    s=f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{bg}"/>'
    if ring: s+=f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{ring}" stroke-width="1.4"/>'
    isz=isize or r*1.25
    return s+ICON(name, cx-isz/2, cy-isz/2, isz, color)
