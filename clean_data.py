# %%
import pandas as pd
import re

# %%
import pandas as pd

# Membaca data dan melewati baris yang rusak
df = pd.read_csv('data_group.csv', encoding='latin1', on_bad_lines='skip')

# Tampilkan beberapa baris pertama untuk memeriksa
print(df.head())


# %%
# Tampilkan kolom-kolom yang ditemukan
print(df.columns)

# Menampilkan beberapa baris untuk melihat data lebih lanjut
print(df.head())


# %%
# Menampilkan beberapa baris pertama untuk memahami struktur data
print(df.head())
# Menampilkan kolom yang ada
print(df.columns)


# %%
# Menghapus kolom yang tidak relevan
df = df.drop(columns=['raw_column', 'other_column'], errors='ignore')

# %%
# Menampilkan nama-nama kolom yang ada dalam DataFrame
print(df.columns)


# %%
# Membaca file CSV dengan encoding 'utf-8-sig' untuk mengabaikan BOM
df = pd.read_csv('data_group.csv', encoding='utf-8-sig', on_bad_lines='skip')
print(df.columns)

# %%
# Menampilkan beberapa baris pertama dari kolom pertama untuk melihat format data
print(df.iloc[:, 0].head())


# %%
# Memisahkan kolom menjadi 'date_time' dan 'message', menangani ketidakkonsistenan dengan expand=True
df[['date_time', 'message']] = df.iloc[:, 0].str.split(' - ', expand=True, n=1)

# Menampilkan hasil sementara untuk memastikan pemisahan
print(df[['date_time', 'message']].head())


# %%
# Memisahkan 'date_time' menjadi tanggal dan waktu
df[['date', 'time']] = df['date_time'].str.split(' ', n=1, expand=True)

# Menampilkan hasil sementara untuk memastikan pemisahan
print(df[['date', 'time']].head())


# %%
# Memisahkan 'message' menjadi 'sender' dan 'message' menggunakan pemisah ': '
df[['sender', 'message']] = df['message'].str.split(': ', n=1, expand=True)

# Menampilkan hasil akhir
print(df[['date', 'time', 'sender', 'message']].head())


# %%
# Mengisi nilai kosong (NaN) dengan string kosong atau placeholder lainnya
df.fillna({'date': '', 'time': '', 'sender': '', 'message': ''}, inplace=True)

# Menampilkan hasil akhir setelah diisi nilai kosong
print(df[['date', 'time', 'sender', 'message']].head())


# %%
# Menghapus karakter ';;' dari kolom message
df['message'] = df['message'].str.replace(';;', '').str.strip()
print(df[['date', 'time', 'sender', 'message']].head())


# %%
# Mengganti karakter yang terdistorsi dengan karakter yang benar
df['message'] = df['message'].str.replace('â€™', "'", regex=False)
df['message'] = df['message'].str.replace('â€œ', '"', regex=False)
df['message'] = df['message'].str.replace('â€', '"', regex=False)
print(df[['date', 'time', 'sender', 'message']].head())


# %%
# Membersihkan karakter aneh yang terdeteksi dengan ekspresi reguler
df['message'] = df['message'].apply(lambda x: re.sub(r'[\x80-\x9f]', '', x) if isinstance(x, str) else x)

# Cek hasilnya
print(df[['date', 'time', 'sender', 'message']].head())

# %%
# Menggunakan errors='replace' untuk menghindari error encoding
df['message'] = df['message'].apply(lambda x: x.encode('utf-8', errors='replace').decode('utf-8', errors='ignore') if isinstance(x, str) else x)

# Cek hasilnya
print(df[['date', 'time', 'sender', 'message']].head())


# %%
# Menghapus baris yang memiliki pesan kosong atau hanya berisi notifikasi grup
df = df[df['message'].str.strip().notna()]  # Menghapus pesan yang kosong
df = df[~df['message'].str.contains("Anda ditambahkan", case=False)]  # Menghapus notifikasi "Anda ditambahkan"
print(df.head())


# %%
# Membersihkan karakter khusus atau simbol yang tidak diinginkan
df['message'] = df['message'].apply(lambda x: re.sub(r'[^a-zA-Z0-9\s\.,?!]', '', x) if isinstance(x, str) else x)

# Cek hasilnya
print(df[['date', 'time', 'sender', 'message']].head())


# %%
# Menghapus baris yang memiliki nilai tidak valid (misalnya ;; di kolom 'date' atau 'time')
df = df[~df['date'].str.contains(';;', na=False)]
df = df[~df['time'].str.contains(';;', na=False)]

# Sekarang coba konversi kembali
df['datetime'] = pd.to_datetime(df['date'] + ' ' + df['time'], errors='coerce', format='%d/%m/%y %H.%M')

# Cek hasilnya
print(df[['datetime', 'sender', 'message']].head())


# %%
# Menghapus kode negara pada nomor telepon (misalnya, +62)
df['sender'] = df['sender'].apply(lambda x: re.sub(r'^\+62', 'ID ', x) if isinstance(x, str) else x)

# Cek hasilnya
print(df[['datetime', 'sender', 'message']].head())


# %%
# Menghapus duplikasi berdasarkan kolom 'datetime', 'sender', dan 'message'
df = df.drop_duplicates(subset=['datetime', 'sender', 'message'])

# Cek hasilnya
print(df[['datetime', 'sender', 'message']].head())


# %%
# Mengisi nilai kosong pada kolom 'message' dengan string 'No message'
df['message'] = df['message'].fillna('No message')

# Cek hasilnya
print(df[['datetime', 'sender', 'message']].head())


# %%
# Menghapus karakter tidak diinginkan dari kolom 'message'
df['message'] = df['message'].str.replace(';;', '', regex=False)

# Cek hasilnya
print(df[['datetime', 'sender', 'message']].head())


# %%
# Hanya ambil angka, huruf, dan tanda baca umum (seperti titik, koma, tanda tanya, dll.)
df['message'] = df['message'].apply(lambda x: re.sub(r'[^a-zA-Z0-9\s.,;!?()-]', '', str(x)))

# Cek hasilnya
print(df[['datetime', 'sender', 'message']].head())

# %%
df['message'] = df['message'].str.lower()

# Cek hasilnya
print(df[['datetime', 'sender', 'message']].head())


# %%
# Menghapus karakter selain angka, huruf, dan tanda baca umum
df['message'] = df['message'].apply(lambda x: re.sub(r'[^a-zA-Z0-9\s.,;!?()-]', '', str(x)))

# Cek hasilnya
print(df[['datetime', 'sender', 'message']].head())


# %%
# Menghapus spasi ekstra di awal, akhir, dan di tengah pesan
df['message'] = df['message'].apply(lambda x: re.sub(r'\s+', ' ', str(x).strip()))

# Cek hasilnya
print(df[['datetime', 'sender', 'message']].head())


# %%
# Menyimpan hasil pembersihan ke file baru
df.to_csv('data_cleaned.csv', index=False)


# %%


