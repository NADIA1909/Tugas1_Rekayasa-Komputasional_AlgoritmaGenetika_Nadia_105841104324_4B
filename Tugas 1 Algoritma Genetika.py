import random
import string

# --- DATASET KAMUS BASA BUGI' ---
kamus_bugis = {
    "SIPAKATAU": "Memanusiakan Manusia",
    "MALEBBI": "Sopan / Mulia",
    "MAPACCING": "Bersih",
    "MABEL1LA": "Jauh",
    "MACAWE": "Dekat",
    "MATANE": "Berat",
    "MALESSE": "Licin",
    "MARICA": "Basah",
    "MASAGALA": "Berlimpah",
    "MARENI": "Cantik"
}

class AlgoritmaGenetika:
    def __init__(self, target):
        self.target = target.upper()
        self.panjang_gen = len(target)
        self.ukuran_populasi = 6
        self.prob_mutasi = 0.1
        self.populasi = []
        self.fitness_populasi = []
        self.parent_terpilih = []
        self.offspring = []

    # 1. Generate Populasi Awal (Acak)
    def bangkitkan_populasi(self):
        self.populasi = []
        for _ in range(self.ukuran_populasi):
            individu = ''.join(random.choice(string.ascii_uppercase) for _ in range(self.panjang_gen))
            self.populasi.append(individu)

    # 2. Hitung Fitness
    def hitung_fitness(self, individu):
        cocok = sum(1 for a, b in zip(individu, self.target) if a == b)
        return cocok / self.panjang_gen

    def evaluasi_semua_fitness(self):
        self.fitness_populasi = [self.hitung_fitness(ind) for ind in self.populasi]

    # 3. Seleksi Roulette Wheel
    def seleksi_roulette(self):
        total_fitness = sum(self.fitness_populasi)
        if total_fitness == 0:
            self.parent_terpilih = random.sample(self.populasi, 2)
            return
        
        prob = [f/total_fitness for f in self.fitness_populasi]
        
        # Hitung Kumulatif
        kumulatif = []
        current = 0
        for p in prob:
            current += p
            kumulatif.append(current)
            
        self.parent_terpilih = []
        for _ in range(2):
            r = random.random()
            for i, c in enumerate(kumulatif):
                if r <= c:
                    self.parent_terpilih.append(self.populasi[i])
                    break

    # 4. Cross Over (One-Point)
    def crossover(self):
        p1, p2 = self.parent_terpilih
        titik = random.randint(1, self.panjang_gen - 1)
        c1 = p1[:titik] + p2[titik:]
        c2 = p2[:titik] + p1[titik:]
        self.offspring = [c1, c2]

    # 5. Mutasi
    def mutasi(self):
        for i in range(len(self.offspring)):
            if random.random() < self.prob_mutasi:
                list_gen = list(self.offspring[i])
                posisi = random.randint(0, self.panjang_gen - 1)
                list_gen[posisi] = random.choice(string.ascii_uppercase)
                self.offspring[i] = ''.join(list_gen)

# --- FUNGSI MENU UTAMA ---
def main():
    ga = None
    target_kata = ""

    while True:
        print("\n" + "="*30)
        print("=== KAMUS BASA BUGI' (GA) ===")
        print("="*30)
        print("1. Tampilkan Kamus")
        print("2. Cari Kata")
        print("3. Jalankan Algoritma Genetika (Inisialisasi)")
        print("4. Tampilkan Populasi")
        print("5. Hasil Fitness")
        print("6. Seleksi Roulette")
        print("7. Cross Over")
        print("8. Mutasi")
        print("9. Generasi Baru")
        print("10. Keluar")
        
        pilihan = input("Pilih menu (1-10): ")

        if pilihan == '1':
            print("\n--- DAFTAR KAMUS ---")
            for k, v in kamus_bugis.items():
                print(f"{k} : {v}")

        elif pilihan == '2':
            cari = input("Masukkan kata Bugis: ").upper()
            if cari in kamus_bugis:
                print(f"Ketemu! {cari} artinna {kamus_bugis[cari]}")
            else:
                print("Ada-ada dé' nassadia ri kamus.")

        elif pilihan == '3':
            target_kata = input("Masukkan kata target polé ri kamus: ").upper()
            if target_kata in kamus_bugis:
                ga = AlgoritmaGenetika(target_kata)
                ga.bangkitkan_populasi()
                print(f"GA Inisialisasi untu' target: {target_kata}")
            else:
                print("Kata dé' gagga ri kamus!")

        elif pilihan == '4':
            if ga:
                print("\n--- POPULASI SAAT INI ---")
                for i, ind in enumerate(ga.populasi):
                    print(f"Individu {i+1}: {ind}")
            else:
                print("Jalankan menu 3 mulo!")

        elif pilihan == '5':
            if ga:
                ga.evaluasi_semua_fitness()
                print("\n--- HASIL FITNESS ---")
                for i, f in enumerate(ga.fitness_populasi):
                    print(f"Individu {i+1} ({ga.populasi[i]}): {f:.2f}")
            else:
                print("Jalankan menu 3 mulo!")

        elif pilihan == '6':
            if ga:
                ga.seleksi_roulette()
                print("\n--- HASIL SELEKSI (PARENT) ---")
                print(f"Parent terpilih: {ga.parent_terpilih}")
            else:
                print("Evaluasi fitness (menu 5) mulo!")

        elif pilihan == '7':
            if ga and ga.parent_terpilih:
                ga.crossover()
                print("\n--- HASIL CROSSOVER (OFFSPRING) ---")
                print(f"Anak baru: {ga.offspring}")
            else:
                print("Seleksi parent (menu 6) mulo!")

        elif pilihan == '8':
            if ga and ga.offspring:
                ga.mutasi()
                print("\n--- HASIL MUTASI ---")
                print(f"Anak setelah mutasi: {ga.offspring}")
            else:
                print("Lakukan crossover (menu 7) mulo!")

        elif pilihan == '9':
            if ga and ga.offspring:
                # Ganti individu terburuk dengan offspring
                for i in range(len(ga.offspring)):
                    min_idx = ga.fitness_populasi.index(min(ga.fitness_populasi))
                    ga.populasi[min_idx] = ga.offspring[i]
                    ga.fitness_populasi[min_idx] = ga.hitung_fitness(ga.offspring[i])
                print("\nGenerasi baru pura dibentuk! Cek menu 4.")
            else:
                print("Selesaikan prosés mutasi mulo!")

        elif pilihan == '10':
            print("Sukkuru', selasai!")
            break
        else:
            print("Pilihan dé' nassadia.")

if __name__ == "__main__":
    main()