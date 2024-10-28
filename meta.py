from metaflow import FlowSpec, step

class KuliahInformatikaFlow(FlowSpec):
    
    @step
    def start(self):
        # Inisialisasi mahasiswa
        self.nama_mahasiswa = "MUjahidin Aljawari"
        self.spp_dibayar = False
        print(f"Memulai alur untuk mahasiswa: {self.nama_mahasiswa}")
        self.next(self.bayar_spp)

    @step
    def bayar_spp(self):
        # Langkah untuk membayar SPP
        self.spp_dibayar = True
        print(f"{self.nama_mahasiswa} telah membayar SPP.")
        self.next(self.mengikuti_kuliah)

    @step
    def mengikuti_kuliah(self):
        # Langkah untuk mengikuti kuliah jika SPP sudah dibayar
        if not self.spp_dibayar:
            print(f"{self.nama_mahasiswa} harus membayar SPP terlebih dahulu.")
            self.next(self.end)
        else:
            print(f"{self.nama_mahasiswa} mengikuti kuliah Informatika.")
            self.next(self.dapatkan_nilai)

    @step
    def dapatkan_nilai(self):
        # Langkah untuk memberikan nilai akhir
        self.nilai_akhir = "A"
        print(f"{self.nama_mahasiswa} mendapatkan nilai akhir: {self.nilai_akhir}")
        self.next(self.end)

    @step
    def end(self):
        # Akhir dari alur kerja
        print("Alur kerja selesai untuk mahasiswa:", self.nama_mahasiswa)

if __name__ == "__main__":
    KuliahInformatikaFlow()
