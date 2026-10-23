import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

os.makedirs("docs/images", exist_ok=True)

# Common styling
plt.rcParams['font.sans-serif'] = 'DejaVu Sans'
plt.rcParams['axes.edgecolor'] = '#CBD5E1'
plt.rcParams['axes.linewidth'] = 0.8

def create_system_architecture_diagram():
    fig, ax = plt.subplots(figsize=(11, 6.5), dpi=300)
    ax.set_xlim(0, 11)
    ax.set_ylim(0, 6.5)
    ax.axis('off')

    # Background canvas
    fig.patch.set_facecolor('#F8FAFC')
    ax.set_facecolor('#F8FAFC')

    # Title
    ax.text(5.5, 6.1, "HE THONG DAT PHONG KHACH SAN - DOCKER ARCHITECTURE", 
            ha='center', va='center', fontsize=12, fontweight='bold', color='#0F172A')
    ax.text(5.5, 5.8, "Sinh vien: Phung Thien Truong (MSSV: DTC245200274) - ICTU", 
            ha='center', va='center', fontsize=9, color='#475569')

    # Client Box
    client_box = patches.FancyBboxPatch((0.4, 3.8), 2.2, 1.4, boxstyle="round,pad=0.15", 
                                       edgecolor="#2563EB", facecolor="#EFF6FF", linewidth=1.5)
    ax.add_patch(client_box)
    ax.text(1.5, 4.7, "Client / User", ha='center', va='center', fontsize=10, fontweight='bold', color='#1E40AF')
    ax.text(1.5, 4.3, "Web Browser (Chrome/Edge)", ha='center', va='center', fontsize=7.5, color='#1E3A8A')
    ax.text(1.5, 4.0, "http://localhost:3001", ha='center', va='center', fontsize=8, fontweight='bold', color='#2563EB')

    # Frontend Container Box
    fe_box = patches.FancyBboxPatch((3.4, 3.8), 2.4, 1.4, boxstyle="round,pad=0.15", 
                                   edgecolor="#0D9488", facecolor="#F0FDFA", linewidth=1.5)
    ax.add_patch(fe_box)
    ax.text(4.6, 4.7, "hotel-frontend", ha='center', va='center', fontsize=10, fontweight='bold', color='#0F766E')
    ax.text(4.6, 4.3, "React 18 + Vite SPA", ha='center', va='center', fontsize=8, color='#115E59')
    ax.text(4.6, 4.0, "Nginx Reverse Proxy /api/", ha='center', va='center', fontsize=7.5, color='#0D9488')

    # Backend Container Box
    be_box = patches.FancyBboxPatch((6.6, 3.8), 2.4, 1.4, boxstyle="round,pad=0.15", 
                                   edgecolor="#D97706", facecolor="#FFFBEB", linewidth=1.5)
    ax.add_patch(be_box)
    ax.text(7.8, 4.7, "hotel-backend", ha='center', va='center', fontsize=10, fontweight='bold', color='#B45309')
    ax.text(7.8, 4.3, "Node.js 20 Express REST", ha='center', va='center', fontsize=8, color='#92400E')
    ax.text(7.8, 4.0, "Metrics /metrics & Pessimistic Lock", ha='center', va='center', fontsize=7.5, color='#B45309')

    # Database Container Box
    db_box = patches.FancyBboxPatch((6.6, 1.2), 2.4, 1.6, boxstyle="round,pad=0.15", 
                                   edgecolor="#4F46E5", facecolor="#EEF2FF", linewidth=1.5)
    ax.add_patch(db_box)
    ax.text(7.8, 2.3, "hotel-postgres", ha='center', va='center', fontsize=10, fontweight='bold', color='#4338CA')
    ax.text(7.8, 1.9, "PostgreSQL 16 Alpine", ha='center', va='center', fontsize=8, color='#3730A3')
    ax.text(7.8, 1.6, "Port: 127.0.0.1:5432", ha='center', va='center', fontsize=7.5, fontweight='bold', color='#4338CA')
    ax.text(7.8, 1.35, "hotel_db (ACID, 3NF)", ha='center', va='center', fontsize=7.5, color='#4F46E5')

    # Observability Stack Box
    obs_box = patches.FancyBboxPatch((0.4, 0.6), 5.4, 2.2, boxstyle="round,pad=0.2", 
                                    edgecolor="#64748B", facecolor="#F1F5F9", linewidth=1.2, linestyle='--')
    ax.add_patch(obs_box)
    ax.text(3.1, 2.5, "Observability & Monitoring Stack", ha='center', va='center', fontsize=9, fontweight='bold', color='#334155')

    # Prometheus
    prom = patches.FancyBboxPatch((0.7, 0.9), 1.5, 1.2, boxstyle="round,pad=0.1", 
                                  edgecolor="#EA580C", facecolor="#FFF7ED", linewidth=1)
    ax.add_patch(prom)
    ax.text(1.45, 1.7, "Prometheus", ha='center', va='center', fontsize=8, fontweight='bold', color='#C2410C')
    ax.text(1.45, 1.3, "Port 9090", ha='center', va='center', fontsize=7, color='#EA580C')
    ax.text(1.45, 1.05, "Scrape Metrics", ha='center', va='center', fontsize=6.5, color='#9A3412')

    # Grafana
    graf = patches.FancyBboxPatch((2.4, 0.9), 1.5, 1.2, boxstyle="round,pad=0.1", 
                                  edgecolor="#F59E0B", facecolor="#FFFBEB", linewidth=1)
    ax.add_patch(graf)
    ax.text(3.15, 1.7, "Grafana", ha='center', va='center', fontsize=8, fontweight='bold', color='#B45309')
    ax.text(3.15, 1.3, "Port 3000", ha='center', va='center', fontsize=7, color='#D97706')
    ax.text(3.15, 1.05, "KPI Dashboards", ha='center', va='center', fontsize=6.5, color='#92400E')

    # Loki + Promtail
    loki = patches.FancyBboxPatch((4.1, 0.9), 1.5, 1.2, boxstyle="round,pad=0.1", 
                                  edgecolor="#0284C7", facecolor="#F0F9FF", linewidth=1)
    ax.add_patch(loki)
    ax.text(4.85, 1.7, "Loki+Promtail", ha='center', va='center', fontsize=8, fontweight='bold', color='#0369A1')
    ax.text(4.85, 1.3, "Port 3100", ha='center', va='center', fontsize=7, color='#0284C7')
    ax.text(4.85, 1.05, "Centralized Logs", ha='center', va='center', fontsize=6.5, color='#075985')

    # Connecting Arrows
    ax.annotate('', xy=(3.4, 4.5), xytext=(2.6, 4.5),
                arrowprops=dict(arrowstyle="->", lw=1.8, color="#2563EB"))
    ax.text(3.0, 4.7, "HTTP", fontsize=7.5, ha='center', color='#2563EB')

    ax.annotate('', xy=(6.6, 4.5), xytext=(5.8, 4.5),
                arrowprops=dict(arrowstyle="->", lw=1.8, color="#0D9488"))
    ax.text(6.2, 4.7, "REST", fontsize=7.5, ha='center', color='#0D9488')

    ax.annotate('', xy=(7.8, 2.8), xytext=(7.8, 3.8),
                arrowprops=dict(arrowstyle="<->", lw=1.8, color="#4F46E5"))
    ax.text(8.3, 3.3, "SQL TCP 5432", fontsize=7.5, ha='left', color='#4F46E5')

    ax.annotate('', xy=(1.45, 2.1), xytext=(7.0, 4.0),
                arrowprops=dict(arrowstyle="->", lw=1.2, color="#EA580C", linestyle='dotted'))
    ax.text(4.5, 3.2, "pull /metrics (RED)", fontsize=7, ha='center', color='#C2410C')

    ax.annotate('', xy=(4.85, 2.1), xytext=(7.4, 3.8),
                arrowprops=dict(arrowstyle="->", lw=1.2, color="#0284C7", linestyle='dotted'))
    ax.text(6.1, 2.8, "docker logs", fontsize=7, ha='center', color='#0369A1')

    plt.tight_layout()
    plt.savefig("docs/images/hinh1_kientruc_hethong.png", dpi=300, bbox_inches='tight')
    plt.close()

def create_database_erd_diagram():
    fig, ax = plt.subplots(figsize=(10.5, 6), dpi=300)
    ax.set_xlim(0, 10.5)
    ax.set_ylim(0, 6)
    ax.axis('off')
    fig.patch.set_facecolor('#FFFFFF')

    ax.text(5.25, 5.7, "SO DO THUC THE QUAN HE (POSTGRESQL 16 - 3NF)", 
            ha='center', va='center', fontsize=11, fontweight='bold', color='#0F172A')

    # Table 1: room_types
    ax.add_patch(patches.FancyBboxPatch((0.5, 3.4), 2.6, 1.8, boxstyle="round,pad=0.1", edgecolor="#1E3A8A", facecolor="#F8FAFC"))
    ax.text(1.8, 4.95, "room_types", ha='center', fontweight='bold', fontsize=9, color='#1E3A8A')
    ax.plot([0.5, 3.1], [4.75, 4.75], color='#CBD5E1', lw=0.8)
    ax.text(0.7, 4.5, "+ id: SERIAL [PK]", fontsize=7.5, color='#0F172A')
    ax.text(0.7, 4.25, "+ code: VARCHAR(20)", fontsize=7.5, color='#475569')
    ax.text(0.7, 4.0, "+ name: VARCHAR(100)", fontsize=7.5, color='#475569')
    ax.text(0.7, 3.75, "+ base_price_vnd: NUMERIC", fontsize=7.5, color='#475569')
    ax.text(0.7, 3.5, "+ capacity: INT", fontsize=7.5, color='#475569')

    # Table 2: rooms
    ax.add_patch(patches.FancyBboxPatch((3.9, 3.4), 2.7, 1.8, boxstyle="round,pad=0.1", edgecolor="#0D9488", facecolor="#F8FAFC"))
    ax.text(5.25, 4.95, "rooms", ha='center', fontweight='bold', fontsize=9, color='#0F766E')
    ax.plot([3.9, 6.6], [4.75, 4.75], color='#CBD5E1', lw=0.8)
    ax.text(4.1, 4.5, "+ id: SERIAL [PK]", fontsize=7.5, color='#0F172A')
    ax.text(4.1, 4.25, "+ room_number: VARCHAR(20)", fontsize=7.5, color='#475569')
    ax.text(4.1, 4.0, "# room_type_id: INT [FK]", fontsize=7.5, color='#0D9488')
    ax.text(4.1, 3.75, "+ floor: INT", fontsize=7.5, color='#475569')
    ax.text(4.1, 3.5, "+ status: VARCHAR(30)", fontsize=7.5, color='#B91C1C')

    # Table 3: customers
    ax.add_patch(patches.FancyBboxPatch((7.4, 3.4), 2.6, 1.8, boxstyle="round,pad=0.1", edgecolor="#4F46E5", facecolor="#F8FAFC"))
    ax.text(8.7, 4.95, "customers", ha='center', fontweight='bold', fontsize=9, color='#4338CA')
    ax.plot([7.4, 10.0], [4.75, 4.75], color='#CBD5E1', lw=0.8)
    ax.text(7.6, 4.5, "+ id: SERIAL [PK]", fontsize=7.5, color='#0F172A')
    ax.text(7.6, 4.25, "+ full_name: VARCHAR(150)", fontsize=7.5, color='#0F172A')
    ax.text(7.6, 4.0, "+ id_card: VARCHAR(50)", fontsize=7.5, color='#475569')
    ax.text(7.6, 3.75, "+ phone: VARCHAR(30)", fontsize=7.5, color='#475569')
    ax.text(7.6, 3.5, "+ email: VARCHAR(150)", fontsize=7.5, color='#475569')

    # Table 4: bookings
    ax.add_patch(patches.FancyBboxPatch((5.7, 0.6), 2.7, 2.0, boxstyle="round,pad=0.1", edgecolor="#EA580C", facecolor="#F8FAFC"))
    ax.text(7.05, 2.35, "bookings", ha='center', fontweight='bold', fontsize=9, color='#C2410C')
    ax.plot([5.7, 8.4], [2.15, 2.15], color='#CBD5E1', lw=0.8)
    ax.text(5.9, 1.95, "+ id: SERIAL [PK]", fontsize=7.5, color='#0F172A')
    ax.text(5.9, 1.7, "+ booking_code: VARCHAR(50)", fontsize=7.5, color='#0F172A')
    ax.text(5.9, 1.45, "# customer_id: INT [FK]", fontsize=7.5, color='#4F46E5')
    ax.text(5.9, 1.2, "+ check_in / check_out: DATE", fontsize=7.5, color='#475569')
    ax.text(5.9, 0.95, "+ total_price_vnd: NUMERIC", fontsize=7.5, color='#475569')
    ax.text(5.9, 0.7, "+ status: VARCHAR(30)", fontsize=7.5, color='#EA580C')

    # Table 5: booking_rooms
    ax.add_patch(patches.FancyBboxPatch((2.2, 0.6), 2.6, 1.8, boxstyle="round,pad=0.1", edgecolor="#0284C7", facecolor="#F8FAFC"))
    ax.text(3.5, 2.15, "booking_rooms", ha='center', fontweight='bold', fontsize=9, color='#0369A1')
    ax.plot([2.2, 4.8], [1.95, 1.95], color='#CBD5E1', lw=0.8)
    ax.text(2.4, 1.7, "+ id: SERIAL [PK]", fontsize=7.5, color='#0F172A')
    ax.text(2.4, 1.45, "# booking_id: INT [FK]", fontsize=7.5, color='#EA580C')
    ax.text(2.4, 1.2, "# room_id: INT [FK]", fontsize=7.5, color='#0D9488')
    ax.text(2.4, 0.95, "+ price_per_night: NUMERIC", fontsize=7.5, color='#475569')

    # Connectors
    ax.annotate('', xy=(3.9, 4.3), xytext=(3.1, 4.3), arrowprops=dict(arrowstyle="->", lw=1.2, color="#0D9488"))
    ax.annotate('', xy=(7.4, 2.6), xytext=(8.7, 3.4), arrowprops=dict(arrowstyle="->", lw=1.2, color="#4F46E5"))
    ax.annotate('', xy=(4.8, 1.4), xytext=(5.7, 1.4), arrowprops=dict(arrowstyle="->", lw=1.2, color="#EA580C"))
    ax.annotate('', xy=(3.5, 2.4), xytext=(4.5, 3.4), arrowprops=dict(arrowstyle="->", lw=1.2, color="#0284C7"))

    plt.tight_layout()
    plt.savefig("docs/images/hinh2_erd_database.png", dpi=300, bbox_inches='tight')
    plt.close()

def create_sequence_flow_diagram():
    fig, ax = plt.subplots(figsize=(10.5, 6), dpi=300)
    ax.set_xlim(0, 10.5)
    ax.set_ylim(0, 6)
    ax.axis('off')
    fig.patch.set_facecolor('#FFFFFF')

    ax.text(5.25, 5.7, "QUY TRINH DAT PHONG & CHONG OVERBOOKING (PESSIMISTIC LOCKING)", 
            ha='center', va='center', fontsize=11, fontweight='bold', color='#0F172A')

    # Lifelines
    actors = [("Client / Guest", 1.2), ("hotel-frontend", 3.7), ("hotel-backend", 6.5), ("hotel-postgres", 9.2)]
    for name, x in actors:
        ax.add_patch(patches.FancyBboxPatch((x-1.0, 4.8), 2.0, 0.6, boxstyle="round,pad=0.1", edgecolor="#1E3A8A", facecolor="#EFF6FF"))
        ax.text(x, 5.1, name, ha='center', va='center', fontsize=8.5, fontweight='bold', color='#1E40AF')
        ax.plot([x, x], [0.5, 4.8], color='#94A3B8', linestyle='--', lw=1)

    # Messages
    msgs = [
        (1.2, 3.7, 4.3, "1. Chon phong & Ngay dat (POST)", "#2563EB"),
        (3.7, 6.5, 3.8, "2. POST /api/bookings", "#0D9488"),
        (6.5, 9.2, 3.3, "3. BEGIN TRANSACTION", "#7C3AED"),
        (6.5, 9.2, 2.8, "4. SELECT ... FOR UPDATE (Lock phong)", "#DC2626"),
        (9.2, 6.5, 2.3, "5. Tra ve trang thai AVAILABLE / OK", "#059669"),
        (6.5, 9.2, 1.8, "6. INSERT bookings & COMMIT", "#2563EB"),
        (6.5, 3.7, 1.3, "7. Tra ve booking_code + VietQR", "#D97706"),
        (3.7, 1.2, 0.8, "8. Hien thi xac nhan don thanh cong", "#2563EB")
    ]

    for x1, x2, y, text, color in msgs:
        ax.annotate('', xy=(x2, y), xytext=(x1, y),
                    arrowprops=dict(arrowstyle="->", lw=1.3, color=color))
        mid_x = (x1 + x2) / 2
        ax.text(mid_x, y + 0.15, text, ha='center', va='bottom', fontsize=7.5, fontweight='bold', color=color)

    plt.tight_layout()
    plt.savefig("docs/images/hinh3_sequence_booking.png", dpi=300, bbox_inches='tight')
    plt.close()

if __name__ == '__main__':
    create_system_architecture_diagram()
    create_database_erd_diagram()
    create_sequence_flow_diagram()
    print("All diagrams generated successfully in docs/images/")
