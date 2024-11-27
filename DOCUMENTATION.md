
## Dokumentasi API Tomkits

### **POST**  -  **Register**

**Endpoint:**  
`POST http://34.101.37.85:8000/auth/register`

**Deskripsi:**  
Endpoint ini digunakan untuk mendaftarkan pengguna baru ke dalam sistem. Pengguna harus menyediakan  `username`,  `email`, dan  `password`  untuk berhasil membuat akun.

**Request Body:**

json

Copy code

`{
    "username": "Paulus Aditya Wicaksono",
    "email": "paulusaditya22@gmail.com",
    "password": "aditya1234"
}` 

**Responses:**

-   **201 Created**  
    Berhasil:
    
    json
    
    Copy code
    
    `{ "message": "User registered successfully." }` 
    
-   **409 Conflict**  
    Gagal (Pengguna sudah ada):
    
    json
    
    Copy code
    
    `{ "error": "User already exists" }` 
    

----------

### **POST**  -  **Login User**

**Endpoint:**  
`POST http://34.101.37.85:8000/auth/login`

**Deskripsi:**  
Endpoint ini digunakan untuk mengautentikasi pengguna yang sudah terdaftar. Pengguna harus memberikan  `email`  dan  `password`  yang valid untuk mendapatkan akses.

**Request Body:**

json

Copy code

`{
    "email": "paulusaditya22@gmail.com",
    "password": "aditya1234"
}` 

**Responses:**

-   **200 OK**  
    Berhasil (Login berhasil):
    
    json
    
    Copy code
    
    `{ "message": "You are logged in.", "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..." }` 
    
-   **400 Bad Request**  
    Gagal (Email atau kata sandi tidak valid):
    
    json
    
    Copy code
    
    `{ "error": "Invalid email or password." }` 
    

----------

### **GET**  -  **Identitas Pengguna (WhoAmI)**

**Endpoint:**  
`GET http://34.101.37.85:8000/auth/whoami`

**Deskripsi:**  
Endpoint ini digunakan untuk mendapatkan informasi pengguna yang sedang login berdasarkan token autentikasi (JWT).

**Responses:**

-   **200 OK**  
    Berhasil:
    
    json
    
    Copy code
    
    `{
        "user_id": "<unique_user_id>",
        "username": "Paulus Aditya Wicaksono",
        "email": "paulusaditya22@gmail.com",
        "created_at": "2024-11-26T14:34:12.000Z"
    }` 
    

**Authorization:**  
Bearer Token  
`<token>`

----------

### **POST**  -  **Regrain Acces**

**Endpoint:**  
`POST http://34.101.37.85:8000/auth/refresh`

**Deskripsi:**  
Endpoint ini digunakan untuk memperbarui token akses (JWT) menggunakan token refresh yang valid.

**Authorization:**  
Bearer Token  
`<token>`

----------

### **POST**  -  **Logout User**

**Endpoint:**  
`POST http://34.101.37.85:8000/auth/logout`

**Deskripsi:**  
Endpoint ini digunakan untuk logout pengguna dengan membatalkan token autentikasi (baik token akses maupun token refresh).

**Authorization:**  
Bearer Token  
`<token>`

----------

### **POST**  -  **Predict**

**Endpoint:**  
`POST http://34.101.37.85:8000/predict/disease`

**Deskripsi:**  
Endpoint ini digunakan untuk memprediksi penyakit pada tanaman berdasarkan gambar yang diunggah. Sistem menggunakan model pembelajaran mesin untuk menganalisis gambar dan memberikan hasil prediksi.

**Request:**

-   **Headers:**  
    `Content-Type: multipart/form-data`  
    `Authorization: Bearer <token>`
    
-   **Body (form-data):**  
    `file: <image-file>`
    

**Responses:**

-   **400 Bad Request**  - Tidak ada file yang diunggah
    
    json
    
    Copy code
    
    `{ "Response Text": "File is required." }` 
    
-   **400 Bad Request**  - Format file tidak valid
    
    json
    
    Copy code
    
    `{ "Response Text": "Invalid file format" }` 
    
-   **400 Bad Request**  - Bukan gambar daun tomat
    
    json
    
    Copy code
    
    `{ "Response Text": "Bukan daun tomat" }` 
    
-   **401 Unauthorized**  - Token kedaluwarsa atau tidak valid
    
    json
    
    Copy code
    
    `{ "Response Text": "Token expired or invalid. Please login again." }` 
    
-   **200 OK**  - Prediksi berhasil
    
    json
    
    Copy code
    
    `{
        "confidence": "98.74%",
        "deskripsi": "Leaf mold is caused by the fungus Passalora fulva, and it affects the leaves, causing them to turn yellow and become moldy.",
        "nama_penyakit": "Leaf_Mold",
        "rekomendasi_product": [
            {
                "active_ingredient": "Propamocarb Hydrochloride",
                "product_image": "https://storage.googleapis.com/tomkits/product/Previcur.png",
                "product_name": "Previcur Flex"
            },
            {
                "active_ingredient": "Chlorothalonil",
                "product_image": "https://storage.googleapis.com/tomkits/product/Daconil_Fungicide.png",
                "product_name": "Daconil Fungicide"
            },
            {
                "active_ingredient": "Bacillus subtilis",
                "product_image": "https://storage.googleapis.com/tomkits/product/Serenade_Garden.png",
                "product_name": "Serenade Garden"
            }
        ],
        "solusi": "Improve air circulation around the plants, prune affected leaves, and apply fungicides like azoxystrobin."
    }` 
    

**Authorization:**  
Bearer Token  
`<token>`

----------

### **GET**  -  **Riwayat Prediksi**

**Endpoint:**  
`GET http://34.101.37.85:8000/predict/history`

**Deskripsi:**  
Endpoint ini digunakan untuk mendapatkan riwayat prediksi penyakit tanaman yang telah dilakukan oleh pengguna yang sedang login.

**Authorization:**  
Bearer Token  
`<token>`

----------

### **GET**  -  **Detail Prediksi Berdasarkan ID**

**Endpoint:**  
`GET http://34.101.37.85:8000/predict/history/{prediction_id}`

**Deskripsi:**  
Endpoint ini memberikan detail dari prediksi tertentu berdasarkan ID prediksi, termasuk nama penyakit, tingkat kepercayaan model, waktu prediksi, dan URL gambar yang digunakan.

**Authorization:**  
Bearer Token  
`<token>`
