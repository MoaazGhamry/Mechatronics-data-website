# 🚀 Quick Deployment Reference

## Your GitHub Repository
- **URL**: https://github.com/mohamedatia2-maker/mechatronics-data
- **Status**: ✅ Code is committed locally, needs push with authentication

## Required Next Steps

### 1️⃣ Push to GitHub (Do This First!)
Choose one method:

**Option A - GitHub CLI (Easiest)**
```powershell
gh auth login
git push origin main
```

**Option B - Personal Access Token**
1. Generate token at: https://github.com/settings/tokens
2. Select `repo` scope
3. Use token as password when pushing

---

### 2️⃣ Set Up Neon Database
1. Create account: https://neon.tech
2. Create new project
3. Copy connection string (looks like):
   ```
   postgresql://user:pass@host.neon.tech/db?sslmode=require
   ```

---

### 3️⃣ Deploy to Render
1. Create account: https://render.com (sign up with GitHub)
2. Create **New Web Service**
3. Connect repository: `mohamedatia2-maker/mechatronics-data`
4. Settings:
   - **Build Command**: `bash build.sh`
   - **Start Command**: `gunicorn mechatronics_hub.wsgi:application`

---

### 4️⃣ Environment Variables for Render

Add these in **Environment** tab:

```
DATABASE_URL = <Your Neon connection string>
SECRET_KEY = <Generate using command below>
ALLOWED_HOSTS = yourapp.onrender.com
DEBUG = False
GEMINI_API_KEY = <Your API key if using AI features>
```

**Generate SECRET_KEY locally:**
```powershell
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

---

### 5️⃣ After Deployment

Create superuser in Render Shell:
```bash
python manage.py createsuperuser
```

---

## 📁 Files Modified/Created

✅ `requirements.txt` - Production dependencies  
✅ `mechatronics_hub/settings.py` - Environment config  
✅ `.env.example` - Environment template  
✅ `build.sh` - Render build script  
✅ `runtime.txt` - Python version  
✅ `.gitignore` - Updated exclusions  

---

## 🆘 Quick Troubleshooting

**Can't push to GitHub?**
→ Use GitHub CLI: `gh auth login`

**Build fails on Render?**
→ Check build logs for specific error

**Database connection error?**
→ Verify `DATABASE_URL` includes `?sslmode=require`

**500 Error after deployment?**
→ Check Render logs, ensure all env vars are set

---

See [walkthrough.md](file:///C:/Users/Moaaz%20Mohamed/.gemini/antigravity/brain/fff1ecd5-dd2f-4e7d-9032-ec5a780477a7/walkthrough.md) for detailed step-by-step instructions.
