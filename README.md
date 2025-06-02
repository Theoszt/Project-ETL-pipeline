# 📚 README.md Lengkap untuk Proyek ETL Pipeline dengan Celery ☕️

Berikut ini saya buatkan README.md lengkap dan terstruktur sesuai contoh yang Anda berikan, dengan penjelasan mendetail tentang proyek ETL pipeline menggunakan Celery, termasuk setup virtual environment, instalasi dependencies, struktur proyek, dan cara menjalankan task chain di `producer.py`.

---

# ETL Pipeline dengan Celery untuk Data Penjualan Cafe ☕️

## 📖 Deskripsi Proyek

Proyek ini mengimplementasikan pipeline ETL (Extract, Transform, Load) menggunakan Celery untuk mengelola proses preprocessing dan feature engineering pada data penjualan cafe. Pipeline ini mengotomatisasi alur kerja data mulai dari pembersihan data mentah, transformasi fitur, hingga persiapan data untuk analisis atau model machine learning.

Data yang digunakan adalah data penjualan cafe yang masih "kotor" (dirty data) dan perlu diproses agar siap digunakan.

---

## 🚀 Fitur Utama

- **Preprocessing Data**: Membersihkan dan menyiapkan data mentah.
- **Feature Engineering**: Membuat fitur baru yang relevan dari data yang sudah diproses.
- **Workflow Terintegrasi**: Menggunakan Celery untuk mengatur task secara terjadwal dan berantai.
- **Modular dan Mudah Dikembangkan**: Setiap tahap dipisahkan dalam modul Python yang terstruktur.
- **Dukungan Multi-Worker**: Menjalankan Celery dengan dua worker berbeda untuk memisahkan beban kerja preprocessing dan feature engineering.

---

## 🗂 Struktur Proyek

| File / Folder            | Deskripsi Singkat                                                                                  |
|-------------------------|--------------------------------------------------------------------------------------------------|
| `dirty_cafe_sales.csv`   | Dataset penjualan cafe yang berisi data mentah yang perlu diproses.                               |
| `pre_processing.py`      | Modul Celery task untuk preprocessing data, termasuk pembersihan dan transformasi awal.           |
| `feature_engineering.py` | Modul Celery task untuk melakukan feature engineering pada data yang sudah diproses.              |
| `producer.py`            | Mendefinisikan pipeline ETL dengan Celery, mengatur task dan mengeksekusi task mengunakan chain.  |
| `task.py`                | Konfigurasi Celery task queue, termasuk exchange, queue, dan routing key untuk pipeline dan utilitas untuk preprocessing dan feature engineering yang digunakan oleh task-task lain.|
| `__init__.py`            | File inisialisasi proyek (kosong atau berisi konfigurasi dasar).                                  |

---

## ⚙️ Instalasi dan Persiapan Lingkungan dengan Virtual Environment (venv)

Agar proyek ini berjalan dengan baik dan terisolasi dari sistem Python global Anda, sangat disarankan menggunakan **virtual environment (venv)**.

### Langkah-langkah membuat dan menggunakan venv:

1. **Buat virtual environment baru:**

   - Di Windows:
     ```bash
     python -m venv venv
     ```

   - Di macOS/Linux:
     ```bash
     python3 -m venv venv
     ```

2. **Aktifkan virtual environment:**

   - Di Windows:
     ```bash
     venv\Scripts\activate
     ```

   - Di macOS/Linux:
     ```bash
     source venv/bin/activate
     ```

---

## 📦 Instalasi Dependencies

Setelah mengaktifkan virtual environment, install dependencies yang dibutuhkan dengan perintah berikut:

```bash
pip install celery kombu numpy pandas pyprog
```

| Paket     | Keterangan                                                                 |
|-----------|-----------------------------------------------------------------------------|
| celery    | Framework task queue untuk menjalankan task asynchronous.                   |
| kombu     | Messaging library yang digunakan oleh Celery.                              |
| numpy     | Library untuk manipulasi data numerik.                                     |
| pandas    | Library untuk manipulasi dan analisis data tabular.                        |
| pyprog    | Library untuk menyimpan data ke RDBMS PostgreSQL.                          |

---

## 🔧 Menyiapkan Broker Message

Celery membutuhkan message broker untuk mengatur antrian task. Anda bisa menggunakan RabbitMQ atau Redis.

- Pastikan broker sudah terinstall dan berjalan.
- Konfigurasi broker di file `task.py` sesuai kebutuhan.

---

## 🛠 Cara Menjalankan Pipeline ETL

### 1. Menjalankan Celery Worker

Pipeline ini menggunakan dua worker Celery yang berbeda untuk memisahkan task preprocessing dan feature engineering.

| Queue           | Perintah menjalankan worker                                                                                      |
|-----------------|-----------------------------------------------------------------------------------------------------------------|
| fitur_engineer  | `celery -A task worker -Q fitur_engineer --hostname=fitureng@%h --loglevel=info -P solo`                          |
| pre_pros       | `celery -A task worker -Q pre_pros --hostname=preproc@%h --loglevel=info -P solo`                                |

#### Penjelasan opsi:

| Opsi                  | Keterangan                                                                                  |
|-----------------------|---------------------------------------------------------------------------------------------|
| `-A task`             | Menunjukkan modul Celery yang digunakan (`tasks.py`).                                       |
| `worker`              | Menjalankan worker Celery.                                                                  |
| `-Q fitur_engineer`   | Queue yang akan didengarkan worker ini (feature engineering).                               |
| `-Q pre_pros`         | Queue yang akan didengarkan worker ini (preprocessing).                                    |
| `--hostname=...`      | Memberikan nama unik pada worker.                                                          |
| `--loglevel=info`     | Menampilkan log dengan level info.                                                         |
| `-P solo`             | Menjalankan worker dengan pool proses tunggal (sesuai kebutuhan).                           |

### 2. Mejalankan Monitoring flower
```bash
celery -A tasks flower --port=5555
```
| Opsi                  | Keterangan                                                                                  |
|-----------------------|---------------------------------------------------------------------------------------------|
|-A tasks	            |Menunjukkan modul Celery yang digunakan (tasks.py).                                          |
|flower	               |Perintah untuk menjalankan Flower.                                                           |
|--port=5555            |Menentukan port web server Flower (default 5555).                                            |
🌐 Mengakses Dashboard Flower
Buka browser dan akses alamat berikut untuk melihat dashboard Flower:
```
http://localhost:5555
```
### 3. Menjalankan Pipeline ETL dengan Task Chain di Producer

Task chain dieksekusi di `producer.py` untuk menjalankan task preprocessing dan feature engineering secara berurutan.

Jalankan perintah berikut:

```bash
python producer.py
```

- Di dalam `producer.py`, task chain akan mengeksekusi task preprocessing terlebih dahulu.
- Setelah selesai, secara otomatis pipeline akan melanjutkan ke feature engineering.
- Dengan cara ini, Anda tidak perlu menjalankan task satu per satu secara manual.

---

## 📋 Penjelasan Modul

| File                | Fungsi                                                                                                  |
|---------------------|--------------------------------------------------------------------------------------------------------|
| `pre_processing.py` | Task Celery untuk membersihkan data mentah dari file CSV, mengatasi missing values, dan transformasi awal. |
| `feature_engineering.py` | Task Celery yang membuat fitur baru berdasarkan data yang sudah diproses, seperti agregasi dan encoding. |
| `producer.py`       | File utama yang menjalankan pipeline ETL dengan memanggil task chain  Mendefinisikan workflow Celery menggunakan `chain` untuk menghubungkan task preprocessing dan feature engineering secara berurutan. |
| `tasks.py`           | Konfigurasi Celery, termasuk pengaturan queue, exchange, dan routing key untuk mengatur task dalam pipeline. |
| `__init__.py`       | File inisialisasi proyek, bisa berisi konfigurasi dasar atau dibiarkan kosong.                         |

---

## 📊 Dataset

- File `dirty_cafe_sales.csv` berisi data penjualan cafe yang masih mentah dan perlu diproses.
- Dataset ini digunakan sebagai input utama pipeline ETL.

---
