<?php

return [
    'driver' => 'pgsql',
    'host' => env('DB_HOST', 'localhost'),
    'port' => env('DB_PORT', '5432'),
    'database' => env('DB_NAME', 'cyberlab'),
    'username' => env('DB_USER', 'postgres'),
    'password' => env('DB_PASSWORD', 'password'),
];
