from abc import ABC, abstractmethod
import logging

logging.basicConfig(
    filename="iot.log",
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


class BaseDevice(ABC):
    factory_name = "Rikkei Smart Factory"
    base_maintenance_cost = 1000000

    def __init__(self, device_code, device_name, operating_hours=0):
        self.device_code = device_code
        self.device_name = device_name
        self.__operating_hours = operating_hours

    @property
    def operating_hours(self):
        return self.__operating_hours

    def add_operating_hours(self, hours):
        self.__operating_hours += hours

    @property
    def device_name(self):
        return self.__device_name

    @device_name.setter
    def device_name(self, value):
        self.__device_name = value.strip().upper()

    @staticmethod
    def validate_device_code(device_code):
        return len(device_code) == 10 and device_code[0].isalpha()

    @classmethod
    def update_maintenance_cost(cls, new_cost):
        cls.base_maintenance_cost = new_cost

    def __add__(self, other):
        if not isinstance(other, BaseDevice):
            raise TypeError(
                "[Lỗi] (ERR-IOT-04): Lỗi kiểu dữ liệu! Không thể thực hiện toán tử với đối tượng ngoài hệ thống."
            )
        return self.operating_hours + other.operating_hours

    def __lt__(self, other):
        if not isinstance(other, BaseDevice):
            raise TypeError(
                "[Lỗi] (ERR-IOT-04): Lỗi kiểu dữ liệu! Không thể thực hiện toán tử với đối tượng ngoài hệ thống."
            )
        return self.operating_hours < other.operating_hours

    @abstractmethod
    def track_performance(self):
        pass

    @abstractmethod
    def run_diagnostic(self):
        pass


class ProductionRobot(BaseDevice):
    def __init__(
        self,
        device_code,
        device_name,
        operating_hours=0,
        completed_products=0
    ):
        super().__init__(device_code, device_name, operating_hours)
        self.completed_products = completed_products

    def track_performance(self):
        if self.operating_hours == 0:
            return 0
        return round(
            (self.completed_products /
             (self.operating_hours * 50)) * 100,
            2
        )

    def run_diagnostic(self):
        if self.completed_products > 10000:
            return "Cảnh báo: Robot cần bảo dưỡng!"
        return "Robot hoạt động bình thường."


class ThermalSensor(BaseDevice):
    def __init__(
        self,
        device_code,
        device_name,
        operating_hours=0,
        current_temperature=25,
        safety_threshold=80
    ):
        super().__init__(device_code, device_name, operating_hours)
        self.current_temperature = current_temperature
        self.safety_threshold = safety_threshold

    def track_performance(self):
        return self.safety_threshold - self.current_temperature

    def run_diagnostic(self):
        if self.current_temperature > self.safety_threshold:
            return (
                f"Nguy hiểm: Vượt ngưỡng nhiệt! "
                f"({self.current_temperature}°C / "
                f"{self.safety_threshold}°C)"
            )
        return "Nhiệt độ an toàn."


class HybridSmartActuator(ProductionRobot, ThermalSensor):
    def __init__(
        self,
        device_code,
        device_name,
        operating_hours=0,
        completed_products=0,
        current_temperature=25,
        safety_threshold=80
    ):
        ProductionRobot.__init__(
            self,
            device_code,
            device_name,
            operating_hours,
            completed_products
        )
        self.current_temperature = current_temperature
        self.safety_threshold = safety_threshold


class MQTTEngineGateway:
    def process_stream(self, device):
        print(
            f"[MQTT] Đã gửi dữ liệu thiết bị "
            f"{device.device_code}"
        )


class ERPReportGateway:
    def process_stream(self, device):
        print(
            f"[ERP] Đã đồng bộ dữ liệu thiết bị "
            f"{device.device_code}"
        )


def export_telemetry_data(data_gateway, device_object):
    if not hasattr(data_gateway, "process_stream"):
        raise AttributeError(
            "[Lỗi] (ERR-IOT-05): Xung đột kiến trúc! "
            "Không thể xuất dữ liệu."
        )

    data_gateway.process_stream(device_object)


devices_list = []
current_device = None

while True:
    print("\n===== RIKKEI SMART FACTORY IOT =====")
    print("1. Đăng ký thiết bị")
    print("2. Xem thông tin thiết bị")
    print("3. Cập nhật vận hành")
    print("4. Chẩn đoán thiết bị")
    print("5. So sánh & cộng giờ chạy")
    print("6. Xuất dữ liệu")
    print("7. Thoát")

    choice = input("Chọn chức năng (1-7): ")

    try:
        if choice == "1":
            print("\n1. Robot")
            print("2. Sensor")
            print("3. Hybrid")

            device_type = input("Chọn loại: ")

            code = input("Nhập mã thiết bị: ")

            if not BaseDevice.validate_device_code(code):
                print(
                    "[Lỗi] (ERR-IOT-01): Mã thiết bị không hợp lệ!"
                )
                continue

            name = input("Nhập tên thiết bị: ")

            if device_type == "1":
                current_device = ProductionRobot(code, name)

            elif device_type == "2":
                current_device = ThermalSensor(code, name)

            elif device_type == "3":
                current_device = HybridSmartActuator(code, name)

            else:
                print("Loại thiết bị không hợp lệ.")
                continue

            devices_list.append(current_device)

            print("[Thành công]: Đăng ký thiết bị!")
            print("Tên:", current_device.device_name)

        elif choice == "2":
            if current_device is None:
                print(
                    "[Lỗi] (ERR-IOT-02): "
                    "Chưa có thiết bị."
                )
                continue

            print("\n--- THÔNG TIN THIẾT BỊ ---")
            print("Loại:", type(current_device).__name__)
            print("Nhà máy:", current_device.factory_name)
            print("Mã:", current_device.device_code)
            print("Tên:", current_device.device_name)
            print("Giờ chạy:",
                  current_device.operating_hours)

            print(
                "\n[Hệ thống MRO]:",
                " -> ".join(
                    cls.__name__
                    for cls in current_device.__class__.__mro__
                )
            )

        elif choice == "3":
            if current_device is None:
                print(
                    "[Lỗi] (ERR-IOT-02): "
                    "Chưa có thiết bị."
                )
                continue

            hours = float(
                input("Nhập số giờ chạy mới: ")
            )

            if hours <= 0:
                raise ValueError

            current_device.add_operating_hours(hours)

            if isinstance(
                current_device,
                ProductionRobot
            ):
                products = int(
                    input("Số sản phẩm mới: ")
                )

                if products < 0:
                    raise ValueError

                current_device.completed_products += products

            result = current_device.track_performance()

            print("[Thành công]")
            print(
                "Tổng giờ:",
                current_device.operating_hours
            )
            print("Hiệu suất:", result)

        elif choice == "4":
            if current_device is None:
                print(
                    "[Lỗi] (ERR-IOT-02): "
                    "Chưa có thiết bị."
                )
                continue

            print(current_device.run_diagnostic())

            print(
                "Chi phí bảo trì:",
                f"{BaseDevice.base_maintenance_cost:,}",
                "VND"
            )

        elif choice == "5":
            if len(devices_list) < 2:
                print("Cần ít nhất 2 thiết bị.")
                continue

            for device in devices_list:
                print(
                    device.device_code,
                    "-",
                    device.device_name
                )

            code = input(
                "Chọn mã thiết bị đối ứng: "
            )

            other = None

            for device in devices_list:
                if device.device_code == code:
                    other = device
                    break

            if other:
                print(
                    "A < B:",
                    current_device < other
                )

                print(
                    "Tổng giờ chạy:",
                    current_device + other
                )

        elif choice == "6":
            if current_device is None:
                print(
                    "[Lỗi] (ERR-IOT-02): "
                    "Chưa có thiết bị."
                )
                continue

            print("1. MQTT")
            print("2. ERP")

            gateway_choice = input("Chọn: ")

            if gateway_choice == "1":
                gateway = MQTTEngineGateway()
            else:
                gateway = ERPReportGateway()

            export_telemetry_data(
                gateway,
                current_device
            )

        elif choice == "7":
            print(
                "Cảm ơn bạn đã sử dụng hệ thống!"
            )
            break

        else:
            print(
                "[Lỗi] (ERR-IOT-06): "
                "Lựa chọn không hợp lệ!"
            )

    except ValueError:
        logging.error(
            "ERR-IOT-03",
            exc_info=True
        )
        print(
            "[Lỗi] (ERR-IOT-03): "
            "Định dạng dữ liệu sai!"
        )

    except Exception as e:
        logging.error(str(e), exc_info=True)
        print(e)