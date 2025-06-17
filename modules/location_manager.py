"""
GPS坐标自动定位模块
支持多种定位方式：IP定位、系统GPS、手动选择
"""
import requests
import json
import platform
import subprocess
import tkinter as tk
from tkinter import messagebox, simpledialog
import webbrowser
from typing import Tuple, Optional, Dict


class LocationManager:
    """位置管理器 - 自动获取和管理GPS坐标"""
    
    def __init__(self):
        self.system = platform.system()
        self.location_apis = {
            'ip_api': 'http://ip-api.com/json/',
            'ipinfo': 'https://ipinfo.io/json',
            'baidu_api': 'https://api.map.baidu.com/location/ip',
            'amap_api': 'https://restapi.amap.com/v3/ip'
        }
    
    def get_location_by_ip(self) -> Optional[Dict]:
        """通过IP地址获取大概位置"""
        try:
            # 尝试多个IP定位服务
            for service, url in self.location_apis.items():
                try:
                    response = requests.get(url, timeout=5)
                    if response.status_code == 200:
                        data = response.json()
                        
                        if service == 'ip_api':
                            if data.get('status') == 'success':
                                return {
                                    'lat': data.get('lat'),
                                    'lng': data.get('lon'),
                                    'city': data.get('city'),
                                    'region': data.get('regionName'),
                                    'country': data.get('country'),
                                    'source': 'IP定位'
                                }
                        elif service == 'ipinfo':
                            if 'loc' in data:
                                lat, lng = data['loc'].split(',')
                                return {
                                    'lat': float(lat),
                                    'lng': float(lng),
                                    'city': data.get('city'),
                                    'region': data.get('region'),
                                    'country': data.get('country'),
                                    'source': 'IP定位'
                                }
                except Exception as e:
                    print(f"IP定位服务 {service} 失败: {e}")
                    continue
            
            return None
        except Exception as e:
            print(f"IP定位失败: {e}")
            return None
    
    def get_system_location(self) -> Optional[Dict]:
        """获取系统GPS位置（需要权限）"""
        try:
            if self.system == "Windows":
                return self._get_windows_location()
            elif self.system == "Darwin":  # macOS
                return self._get_macos_location()
            elif self.system == "Linux":
                return self._get_linux_location()
        except Exception as e:
            print(f"系统GPS定位失败: {e}")
            return None
    
    def _get_windows_location(self) -> Optional[Dict]:
        """Windows系统GPS定位"""
        try:
            # 使用Windows Location API
            import winrt.windows.devices.geolocation as geo
            
            locator = geo.Geolocator()
            # 请求位置权限
            pos = locator.get_geoposition_async().get()
            
            if pos and pos.coordinate:
                return {
                    'lat': pos.coordinate.point.position.latitude,
                    'lng': pos.coordinate.point.position.longitude,
                    'accuracy': pos.coordinate.accuracy,
                    'source': 'Windows GPS'
                }
        except ImportError:
            print("Windows GPS API不可用，请安装winrt包")
        except Exception as e:
            print(f"Windows GPS定位失败: {e}")
        return None
    
    def _get_macos_location(self) -> Optional[Dict]:
        """macOS系统GPS定位"""
        try:
            # 使用CoreLocation框架
            script = '''
            tell application "System Events"
                set location to do shell script "python3 -c \\"
                import CoreLocation
                manager = CoreLocation.CLLocationManager()
                location = manager.location
                if location:
                    print(f'{location.coordinate.latitude},{location.coordinate.longitude}')
                \\""
            end tell
            '''
            result = subprocess.run(['osascript', '-e', script], 
                                  capture_output=True, text=True)
            if result.returncode == 0 and result.stdout.strip():
                lat, lng = result.stdout.strip().split(',')
                return {
                    'lat': float(lat),
                    'lng': float(lng),
                    'source': 'macOS GPS'
                }
        except Exception as e:
            print(f"macOS GPS定位失败: {e}")
        return None
    
    def _get_linux_location(self) -> Optional[Dict]:
        """Linux系统GPS定位"""
        try:
            # 尝试使用geoclue服务
            result = subprocess.run(['gdbus', 'call', '--system',
                                   '--dest', 'org.freedesktop.GeoClue2',
                                   '--object-path', '/org/freedesktop/GeoClue2/Manager',
                                   '--method', 'org.freedesktop.GeoClue2.Manager.GetClient'],
                                  capture_output=True, text=True)
            # 这里需要更复杂的D-Bus交互，简化处理
            return None
        except Exception as e:
            print(f"Linux GPS定位失败: {e}")
        return None
    
    def manual_location_picker(self) -> Optional[Dict]:
        """手动选择位置 - 打开地图选择器"""
        try:
            # 创建简单的GUI选择器
            root = tk.Tk()
            root.withdraw()  # 隐藏主窗口
            
            # 提供几种选择方式
            choice = messagebox.askyesnocancel(
                "位置选择",
                "选择获取位置的方式：\n"
                "是 - 打开腾讯地图坐标拾取器\n"
                "否 - 手动输入坐标\n"
                "取消 - 使用IP定位"
            )
            
            if choice is True:
                # 打开腾讯地图坐标拾取器
                webbrowser.open('https://lbs.qq.com/getPoint/')
                
                # 等待用户输入坐标
                coords = simpledialog.askstring(
                    "坐标输入",
                    "请从腾讯地图复制坐标并粘贴\n格式：纬度,经度"
                )
                
                if coords and ',' in coords:
                    try:
                        lat, lng = coords.split(',')
                        return {
                            'lat': float(lat.strip()),
                            'lng': float(lng.strip()),
                            'source': '手动选择'
                        }
                    except ValueError:
                        messagebox.showerror("错误", "坐标格式不正确")
                        
            elif choice is False:
                # 手动输入
                lat = simpledialog.askfloat("纬度", "请输入纬度（至少8位小数）:")
                lng = simpledialog.askfloat("经度", "请输入经度（至少8位小数）:")
                
                if lat and lng:
                    return {
                        'lat': lat,
                        'lng': lng,
                        'source': '手动输入'
                    }
            
            root.destroy()
            return None
            
        except Exception as e:
            print(f"手动位置选择失败: {e}")
            return None
    
    def get_best_location(self) -> Dict:
        """获取最佳位置信息"""
        print("🌍 正在获取位置信息...")
        
        # 1. 首先尝试系统GPS
        location = self.get_system_location()
        if location:
            print(f"✅ 系统GPS定位成功: {location['source']}")
            return location
        
        # 2. 尝试IP定位
        location = self.get_location_by_ip()
        if location:
            print(f"✅ IP定位成功: {location['source']}")
            print(f"📍 位置: {location.get('city', '')}, {location.get('region', '')}")
            
            # 询问用户是否接受IP定位结果
            try:
                root = tk.Tk()
                root.withdraw()
                
                accept = messagebox.askyesno(
                    "位置确认",
                    f"检测到您的大概位置：\n"
                    f"城市: {location.get('city', '未知')}\n"
                    f"地区: {location.get('region', '未知')}\n"
                    f"坐标: {location['lat']:.6f}, {location['lng']:.6f}\n\n"
                    f"是否使用此位置？\n"
                    f"（选择'否'将打开手动选择）"
                )
                
                root.destroy()
                
                if accept:
                    return location
            except:
                pass
        
        # 3. 手动选择
        print("🎯 请手动选择位置...")
        location = self.manual_location_picker()
        if location:
            return location
        
        # 4. 使用默认位置（北京）
        print("⚠️ 使用默认位置（北京）")
        return {
            'lat': 39.90469700,
            'lng': 116.40717800,
            'city': '北京',
            'source': '默认位置'
        }


def test_location_manager():
    """测试位置管理器"""
    manager = LocationManager()
    location = manager.get_best_location()
    print(f"最终位置: {location}")


if __name__ == "__main__":
    test_location_manager()
