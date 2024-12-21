from collections import deque
import heapq

# Hàm nhập đồ thị
def nhap_do_thi():
    do_thi = {}
    so_dinh = int(input("Nhập số lượng đỉnh: "))
    for _ in range(so_dinh):
        dinh = input("Nhập tên đỉnh: ")
        so_canh = int(input(f"Nhập số lượng cạnh từ đỉnh {dinh}: "))
        canh = {}
        for _ in range(so_canh):
            diem_ke, trong_so = input(f"Nhập điểm kề và trọng số (ví dụ: B 1): ").split()
            canh[diem_ke] = int(trong_so)
        do_thi[dinh] = canh
    
    # In ra đồ thị sau khi nhập
    print("Đồ thị đã nhập:")
    for dinh, canh in do_thi.items():
        print(f"{dinh}: {canh}")
    
    return do_thi


# Hàm nhập heuristic
def nhap_heuristic():
    heuristic = {}
    so_dinh = int(input("Nhập số lượng đỉnh để nhập heuristic: "))
    for _ in range(so_dinh):
        dinh = input("Nhập tên đỉnh: ")
        h = int(input(f"Nhập giá trị heuristic cho đỉnh {dinh}: "))
        heuristic[dinh] = h
    return heuristic

# BFS tìm đường đi từ điểm bắt đầu đến điểm trung gian
def bfs_den_trung_gian(do_thi, diem_bat_dau, diem_trung_gian):
    da_tham = set()
    hang_doi = deque([(diem_bat_dau, [diem_bat_dau])])  # Lưu cả đường đi
    while hang_doi:
        hien_tai, duong_di = hang_doi.popleft()
        if hien_tai == diem_trung_gian:
            return duong_di  # Trả về đường đi từ điểm bắt đầu đến trung gian
        if hien_tai not in da_tham:
            da_tham.add(hien_tai)
            for ke in do_thi[hien_tai]:
                if ke not in da_tham:
                    hang_doi.append((ke, duong_di + [ke]))
    return None  # Không tìm thấy đường đi

# A* tìm đường đi từ điểm trung gian đến điểm đích
def a_sao(do_thi, diem_bat_dau, diem_ket_thuc, heuristic, visited_truoc_do=set()):
    tap_mo = []
    heapq.heappush(tap_mo, (0, diem_bat_dau))  # (f, diem)
    tu_dau = {}
    diem_g = {diem: float('inf') for diem in do_thi}  # g(n): khoảng cách từ diem_bat_dau đến đỉnh hiện tại
    diem_g[diem_bat_dau] = 0

    diem_f = {diem: float('inf') for diem in do_thi}  # f(n) = g(n) + h(n)
    diem_f[diem_bat_dau] = heuristic[diem_bat_dau]

    da_duyet = set(visited_truoc_do)  # Đỉnh đã duyệt trước đó (ví dụ từ BFS)

    while tap_mo:
        _, hien_tai = heapq.heappop(tap_mo)

        if hien_tai == diem_ket_thuc:
            # Xây dựng đường đi từ đích về nguồn
            duong_di = []
            while hien_tai in tu_dau:
                duong_di.append(hien_tai)
                hien_tai = tu_dau[hien_tai]
            duong_di.append(diem_bat_dau)
            return duong_di[::-1]  # Trả về đường đi từ diem_bat_dau đến diem_ket_thuc

        da_duyet.add(hien_tai)  # Đánh dấu đã duyệt

        # Duyệt các đỉnh kề
        for ke, trong_so in do_thi[hien_tai].items():
            if ke not in da_duyet:  # Bỏ qua các đỉnh đã duyệt
                diem_g_tam = diem_g[hien_tai] + trong_so
                if diem_g_tam < diem_g[ke]:  # Tìm đường đi ngắn hơn
                    tu_dau[ke] = hien_tai
                    diem_g[ke] = diem_g_tam
                    diem_f[ke] = diem_g[ke] + heuristic[ke]
                    heapq.heappush(tap_mo, (diem_f[ke], ke))

    return None  # Nếu không tìm thấy đường đi

# Kết hợp BFS và A*
def ket_hop_bfs_a_sao():
    do_thi = nhap_do_thi()  # Nhập đồ thị
    heuristic = nhap_heuristic()  # Nhập heuristic

    diem_bat_dau = input("Nhập điểm bắt đầu: ")
    diem_ket_thuc = input("Nhập điểm kết thúc: ")
    diem_trung_gian = input("Nhập điểm trung gian: ")
    

    # Giai đoạn 1: BFS từ điểm bắt đầu đến điểm trung gian
    duong_di_bfs = bfs_den_trung_gian(do_thi, diem_bat_dau, diem_trung_gian)
    if duong_di_bfs is None:
        print(f"Không tìm thấy đường đi từ {diem_bat_dau} đến {diem_trung_gian}.")
    else:
        print(f"Đường đi từ {diem_bat_dau} đến {diem_trung_gian} (BFS): {' -> '.join(duong_di_bfs)}")

        # Giai đoạn 2: A* từ điểm trung gian đến điểm kết thúc
        duong_di_a_sao = a_sao(do_thi, diem_trung_gian, diem_ket_thuc, heuristic)
        if duong_di_a_sao is None:
            print(f"Không tìm thấy đường đi từ {diem_trung_gian} đến {diem_ket_thuc}.")
        else:
            print(f"Đường đi từ {diem_trung_gian} đến {diem_ket_thuc} (A*): {' -> '.join(duong_di_a_sao)}")

            # Kết hợp đường đi từ BFS và A* (Lưu ý: loại bỏ điểm trung gian trùng lặp ở giữa)
            duong_di_ket_hop = duong_di_bfs + duong_di_a_sao[1:]  # Loại bỏ diem_trung_gian trong duong_di_a_sao
            print(f"Đường đi từ {diem_bat_dau} đến {diem_ket_thuc} (Kết hợp BFS và A*): {' -> '.join(duong_di_ket_hop)}")

# Chạy chương trình
ket_hop_bfs_a_sao()
