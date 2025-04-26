from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Data asal
senarai = []

# Halaman utama
@app.route('/')
def index():
    # Susun ikut markah, dari tinggi ke rendah
    universiti_list = sorted(senarai, key=lambda x: x['markah'], reverse=True)
    return render_template('index.html', universiti_list=universiti_list)

# Tambah universiti
@app.route('/tambah', methods=['POST'])
def tambah():
    nama = request.form['nama'].strip()
    markah = int(request.form['markah'])
    # Pastikan nama tidak sensitif huruf besar kecil
    for universiti in senarai:
        if universiti['nama'].lower() == nama.lower():
            universiti['markah'] = markah
            break
    else:
        senarai.append({'nama': nama, 'markah': markah})
    return redirect(url_for('index'))

# Edit universiti
@app.route('/edit/<nama>', methods=['GET', 'POST'])
def edit(nama):
    if request.method == 'POST':
        markah_baru = int(request.form['markah'])
        for universiti in senarai:
            if universiti['nama'].lower() == nama.lower():
                universiti['markah'] = markah_baru
                break
        return redirect(url_for('index'))
    else:
        # Kalau GET, tunjuk form edit
        for universiti in senarai:
            if universiti['nama'].lower() == nama.lower():
                return '''
                    <h2>Edit Markah Universiti: {}</h2>
                    <form method="post">
                        <input type="number" name="markah" value="{}" required>
                        <button type="submit">Simpan</button>
                    </form>
                    <a href="/">Batal</a>
                '''.format(universiti['nama'], universiti['markah'])
        return 'Universiti tidak dijumpai', 404

# Padam universiti
@app.route('/padam/<nama>')
def padam(nama):
    global senarai
    senarai = [u for u in senarai if u['nama'].lower() != nama.lower()]
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

