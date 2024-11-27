# Tomkits-API Documentation

Berikut adalah dokumentasi Restful API untuk aplikasi Tomkits.

## **POST Register**

### **Endpoint: User Registration**
- **URL**:  
  `http://34.101.37.85:8000/auth/register`  
- **Method**:  
  `POST`  

### **Deskripsi**
Endpoint ini digunakan untuk mendaftarkan pengguna baru ke dalam sistem. Pengguna harus menyediakan data seperti `username`, `email`, dan `password`. Jika pendaftaran berhasil, sistem akan membuat akun baru untuk pengguna tersebut.
- username (string): Nama pengguna yang akan digunakan.
- email (string): Alamat email pengguna.
- password (string): Kata sandi yang akan digunakan untuk login.
---

### **Request Body**
```json
{
    "username": "Paulus Aditya Wicaksono",
    "email": "paulusaditya22@gmail.com",
    "password": "aditya1234"
}
```

### **Response**
- **201 Created (Akun baru berhasil dibuat)**
  ```json
  { "message": "User registered successfully."}
  ```
- **409 Conflict (email atau username sudah dipakai)**
  ```json
  {"error": "User already exists"}
  ```

## **POST Login**

### **Endpoint: Login**
- **URL**:  
  `http://34.101.37.85:8000/auth/login`  
- **Method**:  
  `POST`  

### **Deskripsi**
Endpoint ini digunakan untuk mengautentikasi pengguna yang sudah terdaftar dalam sistem. Pengguna harus memberikan email dan password yang valid untuk mendapatkan akses ke layanan.
- email (string): Alamat email yanng di gunakan untuk registrasi.
- password (string): Kata sandi yang terkait dengan akun.

---

### **Request Body**
```json
{
    "email" : "paulusaditya22@gmail.com",
    "password": "aditya1234"
}
```

### **Response**
- **200 OK (Login Berhasil)**
  ```json
  {
      "message": "You are logged in.",
      "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
  }
  ```
- **400 Bad Request (Login gagal karena email atau kata sandi tidak valid)**
  ```json
  { "error": "Invalid email or password."}
  ```
