@echo off
echo ====================================
echo TechPulse Blog - Local Test Server
echo ====================================
echo.

echo Collecting static files...
python manage.py collectstatic --noinput

echo.
echo Running migrations...
python manage.py migrate

echo.
echo Starting development server...
python manage.py runserver

pause
