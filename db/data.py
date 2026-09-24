import psycopg2

DB_CONFIG = {
    "dbname": "mydatabase",
    "user": "myuser",
    "password": "mypassword",
    "host": "localhost",
    "port": "5432"
}

def seed_database():
    conn = psycopg2.connect(**DB_CONFIG)
    cursor = conn.cursor()

    try:
        # 1. Truncate all tables and reset primary key auto-increment sequences
        print("Xóa toàn bộ dữ liệu cũ và reset ID...")
        cursor.execute("""
            TRUNCATE TABLE provinces, province_roads, province_railways, province_seaports, province_land_use 
            RESTART IDENTITY CASCADE;
        """)

        # 2. Dataset for 10 Vietnamese provinces
        provinces_data = [
            {
                "details": ("Hà Nội", 3358.60, 9.5, 40.0, 1680.00, False, True, True, 8400000, 2022, 2501.04),
                "roads": [("Đại lộ Thăng Long", 29.20), ("Quốc lộ 1A", 45.00), ("Đường vành đai 3", 65.00)],
                "railways": [("Tuyến Hà Nội - Hải Phòng", 102.00), ("Tuyến Cát Linh - Hà Đông", 13.05)],
                "seaports": [],  # Tỉnh/thành phố không giáp biển
                "land_use": [("Đất đô thị", 60000.00, "Khu dân cư và trung tâm hành chính"), ("Đất nông nghiệp", 180000.00, "Trồng lúa và rau màu")]
            },
            {
                "details": ("TP. Hồ Chí Minh", 2095.00, 21.0, 38.5, 1930.00, False, True, True, 9300000, 2022, 4439.14),
                "roads": [("Xa lộ Hà Nội", 15.50), ("Cao tốc TP.HCM - Long Thành", 55.00), ("Quốc lộ 22", 58.00)],
                "railways": [("Tuyến đường sắt Bắc Nam", 14.00), ("Tuyến Metro số 1 (Bến Thành - Suối Tiên)", 19.70)],
                "seaports": [("Cảng Cát Lái", "Cảng container chính"), ("Cảng Hiệp Phước", "Cảng tổng hợp quốc tế")],
                "land_use": [("Đất đô thị", 90000.00, "Khu trung tâm kinh tế và dịch vụ"), ("Đất công nghiệp", 12000.00, "Các khu công nghiệp tập trung")]
            },
            {
                "details": ("Quảng Ninh", 6177.70, 15.0, 36.5, 2200.00, False, True, True, 1320000, 2022, 213.67),
                "roads": [("Quốc lộ 18", 120.50), ("Cao tốc Hạ Long - Móng Cái", 175.80)],
                "railways": [("Tuyến đường sắt Kép - Hạ Long", 106.00)],
                "seaports": [("Cảng Cẩm Phả", "Cảng hàng hóa"), ("Cảng Quốc tế Tần Cảng - Móng Cái", "Cảng thương mại")],
                "land_use": [("Đất lâm nghiệp", 330000.00, "Rừng phòng hộ và rừng sản xuất"), ("Đất đô thị", 45000.00, "Khu dân cư và dịch vụ du lịch")]
            },
            {
                "details": ("Hải Phòng", 1527.40, 13.0, 38.0, 1600.00, False, True, True, 2080000, 2022, 1361.82),
                "roads": [("Cao tốc Hà Nội - Hải Phòng", 105.50), ("Quốc lộ 10", 52.00)],
                "railways": [("Tuyến đường sắt Hà Nội - Hải Phòng (Đoạn nội thành)", 25.00)],
                "seaports": [("Cảng Lạch Huyện", "Cảng cửa ngõ quốc tế"), ("Cảng Hải Phòng", "Cảng tổng hợp")],
                "land_use": [("Đất công nghiệp", 25000.00, "Khu kinh tế Đình Vũ - Cát Hải"), ("Đất nuôi trồng thủy sản", 12000.00, "Nuôi hải sản ven biển")]
            },
            {
                "details": ("Lâm Đồng", 9783.30, 10.5, 28.0, 1750.00, True, False, False, 1310000, 2022, 133.90),
                "roads": [("Quốc lộ 20", 264.00), ("Quốc lộ 27", 180.00), ("Đèo Ngoạn Mục", 20.50)],
                "railways": [("Tuyến Đà Lạt - Trại Mát", 7.00)],
                "seaports": [],
                "land_use": [("Đất nông nghiệp", 300000.00, "Trồng cà phê, trà và rau hoa sạch"), ("Đất bảo tồn thiên nhiên", 520000.00, "Vườn quốc gia Bidoup - Núi Bà")]
            },
            {
                "details": ("Đà Nẵng", 1284.90, 19.0, 39.0, 2500.50, False, True, True, 1220000, 2022, 949.49),
                "roads": [("Quốc lộ 1A", 40.00), ("Cao tốc Đà Nẵng - Quảng Ngãi", 139.20)],
                "railways": [("Tuyến đường sắt Bắc Nam", 30.00), ("Ga Đà Nẵng", 5.00)],
                "seaports": [("Cảng Tiên Sa", "Cảng tổng hợp quốc tế"), ("Cảng Liên Chiểu", "Cảng container chính")],
                "land_use": [("Đất thương mại dịch vụ", 15000.00, "Khu du lịch sinh thái ven biển"), ("Đất công nghiệp", 8000.00, "Khu công nghiệp Hòa Khánh")]
            },
            {
                "details": ("Nghệ An", 16489.90, 8.0, 41.5, 1400.00, True, True, True, 3370000, 2022, 204.37),
                "roads": [("Đường Hồ Chí Minh", 132.00), ("Quốc lộ 7", 225.00)],
                "railways": [("Tuyến đường sắt Bắc Nam (Đoạn Nghệ An)", 94.00)],
                "seaports": [("Cảng Cửa Lò", "Cảng hàng hóa tổng hợp"), ("Cảng Đông Hồi", "Cảng chuyên dùng")],
                "land_use": [("Đất nông nghiệp", 800000.00, "Trồng lúa và cây công nghiệp"), ("Đất nuôi trồng thủy sản", 25000.00, "Nuôi tôm nước lợ")]
            },
            {
                "details": ("Thừa Thiên Huế", 4902.40, 11.0, 40.5, 2800.00, False, True, True, 1150000, 2022, 234.58),
                "roads": [("Quốc lộ 1A", 112.00), ("Đường cao tốc Cam Lộ - La Sơn", 98.30)],
                "railways": [("Tuyến đường sắt Bắc Nam (Đoạn Huế)", 111.00)],
                "seaports": [("Cảng Chân Mây", "Cảng tổng hợp và du lịch"), ("Cảng Thuận An", "Cảng nội địa")],
                "land_use": [("Đất di tích lịch sử", 5000.00, "Quần thể di tích Cố đô Huế"), ("Đất lâm nghiệp", 310000.00, "Rừng đặc dụng và phòng hộ")]
            },
            {
                "details": ("Khánh Hòa", 5137.80, 16.0, 38.0, 1300.00, True, True, False, 1250000, 2022, 243.30),
                "roads": [("Quốc lộ 1A", 150.00), ("Quốc lộ 26", 151.00)],
                "railways": [("Tuyến đường sắt Bắc Nam (Đoạn Khánh Hòa)", 149.00)],
                "seaports": [("Cảng Cam Ranh", "Cảng nước sâu thương mại"), ("Cảng Nha Trang", "Cảng khách du lịch")],
                "land_use": [("Đất du lịch", 22000.00, "Khu nghỉ dưỡng ven biển Nha Trang & Cam Ranh"), ("Đất lâm nghiệp", 240000.00, "Rừng tự nhiên")]
            },
            {
                "details": ("Kiên Giang", 6348.80, 22.0, 35.0, 2100.00, False, True, True, 1730000, 2022, 272.49),
                "roads": [("Quốc lộ 80", 128.00), ("Quốc lộ 61", 96.00), ("Đường hành lang ven biển", 115.00)],
                "railways": [],
                "seaports": [("Cảng Rạch Giá", "Cảng hành khách nội địa"), ("Cảng An Thới (Phú Quốc)", "Cảng du lịch quốc tế")],
                "land_use": [("Đất lúa", 340000.00, "Vùng sản xuất lúa trọng điểm"), ("Đất du lịch nghỉ dưỡng", 18000.00, "Khu du lịch Đảo Phú Quốc")]
            }
        ]

        # Insert SQL statements
        query_province = """
            INSERT INTO provinces (
                name, area_sq_km, min_temp_c, max_temp_c, avg_rainfall_mm,
                has_drought_risk, has_tropical_storm_risk, has_flood_inundation_risk,
                population, population_year, population_density_per_sq_km
            ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id;
        """

        query_road = "INSERT INTO province_roads (province_id, name, length_km) VALUES (%s, %s, %s);"
        query_railway = "INSERT INTO province_railways (province_id, name, length_km) VALUES (%s, %s, %s);"
        query_seaport = "INSERT INTO province_seaports (province_id, name, port_type) VALUES (%s, %s, %s);"
        query_land_use = "INSERT INTO province_land_use (province_id, purpose, area_ha, details) VALUES (%s, %s, %s, %s);"

        # 3. Populate data
        print("Đang chèn dữ liệu mới cho 10 tỉnh thành...")
        for item in provinces_data:
            cursor.execute(query_province, item["details"])
            province_id = cursor.fetchone()[0]

            for road in item["roads"]:
                cursor.execute(query_road, (province_id, *road))

            for rail in item["railways"]:
                cursor.execute(query_railway, (province_id, *rail))

            for port in item["seaports"]:
                cursor.execute(query_seaport, (province_id, *port))

            for land in item["land_use"]:
                cursor.execute(query_land_use, (province_id, *land))

        conn.commit()
        print("Hoàn tất! Đã xóa toàn bộ dữ liệu cũ và chèn 10 tỉnh thành mới thành công.")

    except Exception as e:
        conn.rollback()
        print(f"Lỗi khi thực thi: {e}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    seed_database()