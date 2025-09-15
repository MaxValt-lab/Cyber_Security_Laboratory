<?php

class Security {
    private static $rateLimits = [];
    private static $suspiciousActivity = [];

    // Инициализация защиты
    public static function init() {
        session_start();
        self::checkCSRF();
        self::rateLimiting();
        self::checkHTTPS();
    }

    // Защита от CSRF
    private static function checkCSRF() {
        if (isset($_POST['csrf_token'])) {
            if (hash_equals($_SESSION['csrf_token'], $_POST['csrf_token'])) {
                return true;
            }
            die('CSRF атака');
        }
    }

    // Rate Limiting
    private static function rateLimiting() {
        $ip = $_SERVER['REMOTE_ADDR'];
        if (!isset(self::$rateLimits[$ip])) {
            self::$rateLimits[$ip] = ['count' => 1, 'time' => time()];
        } else {
            if (time() - self::$rateLimits[$ip]['time'] < 60) {
                self::$rateLimits[$ip]['count']++;
                if (self::$rateLimits[$ip]['count'] > 10) {
                    die('Слишком много запросов');
                }
            } else {
                self::$rateLimits[$ip] = ['count' => 1, 'time' => time()];
            }
        }
    }

    // Проверка HTTPS
    private static function checkHTTPS() {
        if (!isset($_SERVER['HTTPS']) || $_SERVER['HTTPS'] !== 'on') {
            header('Location: https://' . $_SERVER['HTTP_HOST'] . $_SERVER['REQUEST_URI']);
            exit;
        }
    }

    // Генерация CSRF токена
    public static function generateCSRFToken() {
        $_SESSION['csrf_token'] = bin2hex(random_bytes(32));
        return $_SESSION['csrf_token'];
    }
}
