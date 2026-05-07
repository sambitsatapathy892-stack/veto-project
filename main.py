from datetime import datetime
from urllib.parse import urlparse

from flask import Flask, render_template_string, request, redirect, url_for
from scraper import analyze

app = Flask(__name__)

TRENDING_ITEMS = [
    "Jio Fiber",
    "boAt Airdopes",
    "Zomato",
    "BYJU'S",
    "OYO Rooms",
    "Redmi",
    "Airtel",
    "Ola",
    "Swiggy",
    "OnePlus",
]

PAGE_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>
    <meta name="description" content="{{ description }}">
    <meta name="theme-color" content="#f8fbff">
    <style>
        :root{
            --bg:#f8fbff;
            --bg-2:#eef5ff;
            --surface:rgba(255,255,255,0.76);
            --surface-strong:#ffffff;
            --line:#d8e5f3;
            --line-2:#c5d8ee;
            --text:#0f172a;
            --muted:#64748b;
            --blue:#2563eb;
            --blue-2:#3b82f6;
            --blue-3:#60a5fa;
            --blue-soft:#dbeafe;
            --green:#16a34a;
            --orange:#ea580c;
            --red:#dc2626;
            --shadow:0 18px 50px rgba(15,23,42,0.08);
            --shadow-lg:0 30px 90px rgba(37,99,235,0.12);
            --radius-xl:38px;
            --radius-lg:26px;
            --radius-md:20px;
            --radius-sm:14px;
            --max:1180px;
        }

        *{
            box-sizing:border-box;
        }

        html{
            scroll-behavior:smooth;
        }

        body{
            margin:0;
            font-family:Inter,"Segoe UI",Arial,sans-serif;
            color:var(--text);
            background:
                radial-gradient(circle at top left, rgba(37,99,235,0.10), transparent 22%),
                radial-gradient(circle at top right, rgba(96,165,250,0.12), transparent 18%),
                linear-gradient(180deg, #fbfdff 0%, #f4f8fe 100%);
        }

        a{
            color:inherit;
            text-decoration:none;
        }

        .ambient{
            position:fixed;
            inset:0;
            pointer-events:none;
            overflow:hidden;
            z-index:-1;
        }

        .blob{
            position:absolute;
            border-radius:50%;
            filter:blur(12px);
            opacity:.62;
            animation:floatBlob 12s ease-in-out infinite;
        }

        .blob.one{
            width:300px;
            height:300px;
            left:-80px;
            top:110px;
            background:radial-gradient(circle, rgba(37,99,235,0.18), transparent 66%);
        }

        .blob.two{
            width:220px;
            height:220px;
            right:30px;
            top:140px;
            background:radial-gradient(circle, rgba(59,130,246,0.16), transparent 66%);
            animation-delay:2s;
        }

        .blob.three{
            width:260px;
            height:260px;
            right:-90px;
            bottom:70px;
            background:radial-gradient(circle, rgba(14,165,233,0.12), transparent 68%);
            animation-delay:4s;
        }

        @keyframes floatBlob{
            0%{transform:translateY(0) translateX(0) scale(1);}
            50%{transform:translateY(-18px) translateX(10px) scale(1.04);}
            100%{transform:translateY(0) translateX(0) scale(1);}
        }

        .container{
            width:min(var(--max), calc(100% - 28px));
            margin:0 auto;
        }

        .site-header{
            position:sticky;
            top:0;
            z-index:70;
            background:rgba(255,255,255,0.72);
            backdrop-filter:blur(16px);
            border-bottom:1px solid rgba(197,216,238,0.55);
        }

        .nav{
            display:flex;
            align-items:center;
            justify-content:space-between;
            gap:18px;
            padding:15px 0;
        }

        .brand{
            display:flex;
            align-items:center;
            gap:12px;
        }

        .brand-mark{
            width:44px;
            height:44px;
            border-radius:15px;
            display:grid;
            place-items:center;
            color:#fff;
            font-weight:800;
            background:linear-gradient(135deg, var(--blue), var(--blue-2));
            box-shadow:0 14px 30px rgba(37,99,235,0.18);
        }

        .brand-copy{
            font-weight:800;
            letter-spacing:.3px;
        }

        .brand-copy small{
            display:block;
            margin-top:3px;
            color:var(--muted);
            font-size:12px;
            font-weight:600;
        }

        .nav-links{
            display:flex;
            align-items:center;
            gap:8px;
            flex-wrap:wrap;
        }

        .nav-link{
            padding:10px 14px;
            border-radius:999px;
            color:var(--muted);
            font-size:14px;
            font-weight:700;
            transition:all .18s ease;
        }

        .nav-link:hover{
            color:var(--text);
            background:rgba(37,99,235,0.06);
        }

        .nav-cta{
            color:#fff;
            background:linear-gradient(135deg, var(--blue), var(--blue-2));
            box-shadow:0 10px 24px rgba(37,99,235,0.16);
        }

        .page-shell{
            min-height:calc(100vh - 140px);
        }

        .hero{
            padding:74px 0 28px;
        }

        .hero-grid{
            display:grid;
            grid-template-columns:1.02fr 0.98fr;
            gap:22px;
            align-items:center;
        }

        .glass,
        .summary-card,
        .action-card,
        .section-card,
        .cta-card,
        .info-card,
        .empty-card{
            background:var(--surface);
            backdrop-filter:blur(14px);
            border:1px solid rgba(216,229,243,0.82);
            box-shadow:var(--shadow);
            border-radius:var(--radius-lg);
        }

        .hero-copy{
            padding:34px 12px 34px 4px;
        }

        .eyebrow{
            display:inline-flex;
            align-items:center;
            gap:8px;
            padding:8px 12px;
            border-radius:999px;
            background:#eff6ff;
            border:1px solid #d7e7ff;
            color:#1d4ed8;
            font-size:12px;
            font-weight:800;
            letter-spacing:.8px;
            text-transform:uppercase;
        }

        .hero-title{
            margin:20px 0 12px;
            font-size:clamp(48px, 8vw, 88px);
            line-height:.90;
            letter-spacing:-3px;
            max-width:760px;
        }

        .hero-title .accent{
            display:block;
            color:var(--blue);
        }

        .hero-sub{
            margin:0;
            max-width:560px;
            color:var(--muted);
            font-size:17px;
            line-height:1.78;
        }

        .search-shell,
        .inline-search{
            display:flex;
            align-items:center;
            gap:10px;
            padding:10px;
            background:var(--surface-strong);
            border:1px solid var(--line);
            border-radius:20px;
            box-shadow:0 18px 40px rgba(37,99,235,0.08);
        }

        .search-shell{
            margin-top:26px;
            max-width:660px;
        }

        .search-shell input,
        .inline-search input{
            flex:1;
            border:none;
            outline:none;
            background:transparent;
            color:var(--text);
            font-size:16px;
            padding:14px 16px;
        }

        .search-shell input::placeholder,
        .inline-search input::placeholder{
            color:#8a9ab4;
        }

        .btn,
        .search-shell button,
        .inline-search button,
        .link-btn{
            border:none;
            outline:none;
            cursor:pointer;
            color:#fff;
            font-weight:800;
            font-size:14px;
            padding:14px 18px;
            border-radius:14px;
            background:linear-gradient(135deg, var(--blue), var(--blue-2));
            box-shadow:0 14px 30px rgba(37,99,235,0.18);
            transition:transform .18s ease, box-shadow .18s ease, filter .18s ease;
            position:relative;
            overflow:hidden;
        }

        .btn::before,
        .search-shell button::before,
        .inline-search button::before,
        .link-btn::before{
            content:"";
            position:absolute;
            top:0;
            left:-120%;
            width:80%;
            height:100%;
            background:linear-gradient(90deg, transparent, rgba(255,255,255,.35), transparent);
            transform:skewX(-20deg);
            transition:left .55s ease;
        }

        .btn:hover::before,
        .search-shell button:hover::before,
        .inline-search button:hover::before,
        .link-btn:hover::before{
            left:140%;
        }

        .btn:hover,
        .search-shell button:hover,
        .inline-search button:hover,
        .link-btn:hover{
            transform:translateY(-2px);
            box-shadow:0 18px 36px rgba(37,99,235,0.24);
            filter:saturate(1.06);
        }

        .micro-row{
            margin-top:18px;
            display:flex;
            flex-wrap:wrap;
            gap:10px;
        }

        .micro-pill,
        .chip{
            display:inline-flex;
            align-items:center;
            gap:8px;
            padding:10px 14px;
            border-radius:999px;
            background:#fff;
            border:1px solid var(--line);
            color:var(--text);
            font-size:14px;
            font-weight:700;
            transition:all .18s ease;
        }

        .micro-pill{
            color:var(--muted);
            font-size:13px;
        }

        .chip:hover{
            transform:translateY(-2px);
            border-color:#bdd6ff;
            background:#f8fbff;
            box-shadow:0 10px 22px rgba(37,99,235,0.08);
        }

        .hero-scene-wrap{
            perspective:1400px;
            height:540px;
            display:flex;
            align-items:center;
            justify-content:center;
        }

        .hero-scene{
            position:relative;
            width:min(520px, 100%);
            height:520px;
            transform-style:preserve-3d;
            transition:transform .18s ease;
        }

        .scene-core{
            position:absolute;
            inset:50% auto auto 50%;
            width:260px;
            height:260px;
            transform:translate(-50%, -50%);
            border-radius:50%;
            background:
                radial-gradient(circle at 35% 30%, #ffffff 0%, #eaf4ff 22%, #bfdcff 55%, #8ab9ff 74%, #4f8fff 100%);
            box-shadow:
                inset -18px -24px 40px rgba(255,255,255,.45),
                inset 24px 18px 48px rgba(255,255,255,.65),
                0 30px 80px rgba(37,99,235,.24);
            animation:orbFloat 8s ease-in-out infinite;
        }

        .scene-core::before{
            content:"";
            position:absolute;
            inset:12%;
            border-radius:50%;
            border:1px solid rgba(255,255,255,.55);
        }

        .scene-core::after{
            content:"";
            position:absolute;
            width:110px;
            height:110px;
            left:26px;
            top:24px;
            border-radius:50%;
            background:radial-gradient(circle, rgba(255,255,255,.95), rgba(255,255,255,0));
            opacity:.7;
            filter:blur(6px);
        }

        .scene-ring{
            position:absolute;
            inset:50% auto auto 50%;
            border-radius:50%;
            border:1.6px solid rgba(37,99,235,.20);
            transform-style:preserve-3d;
        }

        .scene-ring.ring-a{
            width:370px;
            height:370px;
            transform:translate(-50%, -50%) rotateX(72deg) rotateY(8deg);
            animation:ringSpinA 11s linear infinite;
        }

        .scene-ring.ring-b{
            width:420px;
            height:420px;
            transform:translate(-50%, -50%) rotateY(68deg) rotateZ(12deg);
            animation:ringSpinB 13s linear infinite;
        }

        .scene-ring.ring-c{
            width:470px;
            height:470px;
            transform:translate(-50%, -50%) rotateX(86deg) rotateZ(12deg);
            border-color:rgba(96,165,250,.18);
            animation:ringSpinC 16s linear infinite;
        }

        .orbit-dot{
            position:absolute;
            width:18px;
            height:18px;
            border-radius:50%;
            background:linear-gradient(135deg, #ffffff, #93c5fd);
            box-shadow:0 10px 22px rgba(37,99,235,.20);
        }

        .orbit-dot.one{
            top:72px;
            left:95px;
            animation:dotFloat 5s ease-in-out infinite;
        }

        .orbit-dot.two{
            right:92px;
            top:130px;
            width:24px;
            height:24px;
            animation:dotFloat 6s ease-in-out infinite 1s;
        }

        .orbit-dot.three{
            bottom:92px;
            left:108px;
            width:16px;
            height:16px;
            animation:dotFloat 7s ease-in-out infinite 2s;
        }

        @keyframes orbFloat{
            0%{transform:translate(-50%, -50%) translateY(0);}
            50%{transform:translate(-50%, -50%) translateY(-12px);}
            100%{transform:translate(-50%, -50%) translateY(0);}
        }

        @keyframes ringSpinA{
            from{transform:translate(-50%, -50%) rotateX(72deg) rotateY(8deg) rotateZ(0deg);}
            to{transform:translate(-50%, -50%) rotateX(72deg) rotateY(8deg) rotateZ(360deg);}
        }

        @keyframes ringSpinB{
            from{transform:translate(-50%, -50%) rotateY(68deg) rotateZ(0deg);}
            to{transform:translate(-50%, -50%) rotateY(68deg) rotateZ(360deg);}
        }

        @keyframes ringSpinC{
            from{transform:translate(-50%, -50%) rotateX(86deg) rotateZ(0deg);}
            to{transform:translate(-50%, -50%) rotateX(86deg) rotateZ(360deg);}
        }

        @keyframes dotFloat{
            0%{transform:translateY(0);}
            50%{transform:translateY(-10px);}
            100%{transform:translateY(0);}
        }

        .scene-card{
            position:absolute;
            background:rgba(255,255,255,.82);
            backdrop-filter:blur(14px);
            border:1px solid rgba(216,229,243,.82);
            box-shadow:0 20px 45px rgba(37,99,235,.10);
            border-radius:22px;
            transform-style:preserve-3d;
        }

        .scene-card.card-a{
            left:8px;
            top:42px;
            width:220px;
            padding:18px;
            animation:floatCard 8s ease-in-out infinite;
        }

        .scene-card.card-b{
            right:12px;
            top:84px;
            width:190px;
            padding:16px;
            animation:floatCard 8s ease-in-out infinite 1.6s;
        }

        .scene-card.card-c{
            left:32px;
            bottom:48px;
            width:240px;
            padding:16px;
            animation:floatCard 8s ease-in-out infinite 3.1s;
        }

        @keyframes floatCard{
            0%{transform:translateY(0px) translateZ(0);}
            50%{transform:translateY(-10px) translateZ(18px);}
            100%{transform:translateY(0px) translateZ(0);}
        }

        .tiny-label{
            display:block;
            color:var(--muted);
            font-size:11px;
            font-weight:800;
            text-transform:uppercase;
            letter-spacing:.8px;
            margin-bottom:8px;
        }

        .scene-big{
            display:flex;
            align-items:center;
            justify-content:space-between;
            gap:12px;
            margin-bottom:10px;
        }

        .scene-big strong{
            font-size:22px;
            letter-spacing:-.5px;
        }

        .scene-badge{
            min-width:70px;
            height:70px;
            border-radius:22px;
            display:grid;
            place-items:center;
            color:#fff;
            font-size:24px;
            font-weight:800;
            background:linear-gradient(135deg, var(--blue), var(--blue-2));
            box-shadow:0 14px 28px rgba(37,99,235,.18);
        }

        .scene-line{
            padding:10px 12px;
            border-radius:14px;
            background:#fff;
            border:1px solid var(--line);
            color:var(--muted);
            font-size:13px;
            font-weight:700;
            margin-top:8px;
        }

        .scene-line b{
            color:var(--text);
        }

        .section{
            padding:18px 0;
        }

        .section-head{
            margin-bottom:16px;
        }

        .section-head.row{
            display:flex;
            align-items:flex-end;
            justify-content:space-between;
            gap:16px;
        }

        .section-title{
            margin:10px 0 0;
            font-size:clamp(28px, 4vw, 42px);
            letter-spacing:-1px;
        }

        .section-sub{
            margin:0;
            color:var(--muted);
            line-height:1.72;
        }

        .feature-grid{
            display:grid;
            grid-template-columns:repeat(3, 1fr);
            gap:14px;
        }

        .info-card{
            padding:22px;
            transition:transform .22s ease, box-shadow .22s ease;
        }

        .info-card:hover{
            transform:translateY(-5px);
            box-shadow:0 24px 50px rgba(37,99,235,0.10);
        }

        .icon-box{
            width:44px;
            height:44px;
            border-radius:14px;
            display:grid;
            place-items:center;
            margin-bottom:14px;
            background:#eff6ff;
            color:var(--blue);
            font-size:18px;
        }

        .info-card h3{
            margin:0 0 8px;
            font-size:18px;
            letter-spacing:-.4px;
        }

        .info-card p{
            margin:0;
            color:var(--muted);
            font-size:14px;
            line-height:1.68;
        }

        .cta-card{
            padding:26px 28px;
            display:flex;
            align-items:center;
            justify-content:space-between;
            gap:18px;
            box-shadow:var(--shadow-lg);
            background:linear-gradient(135deg, rgba(255,255,255,0.96), rgba(239,246,255,0.90));
        }

        .cta-card h3{
            margin:0 0 6px;
            font-size:24px;
            letter-spacing:-.6px;
        }

        .cta-card p{
            margin:0;
            color:var(--muted);
        }

        .back-link{
            display:inline-flex;
            align-items:center;
            gap:8px;
            color:#1d4ed8;
            font-size:14px;
            font-weight:800;
            margin-bottom:16px;
        }

        .result-head{
            display:flex;
            align-items:flex-start;
            justify-content:space-between;
            gap:18px;
            margin-bottom:18px;
        }

        .page-title{
            margin:12px 0 8px;
            font-size:clamp(36px, 5vw, 60px);
            line-height:.98;
            letter-spacing:-1.8px;
        }

        .page-sub{
            margin:0;
            color:var(--muted);
            line-height:1.7;
        }

        .inline-search{
            width:min(420px, 100%);
        }

        .summary-card{
            padding:28px;
            margin-bottom:14px;
        }

        .score-wrap{
            display:flex;
            align-items:center;
            gap:24px;
            flex-wrap:wrap;
        }

        .score-ring{
            width:160px;
            height:160px;
            border-radius:50%;
            display:grid;
            place-items:center;
            background:conic-gradient(var(--ring) 0deg, #e2e8f0 0deg);
            box-shadow:0 16px 36px rgba(15,23,42,0.10);
        }

        .score-ring-inner{
            width:120px;
            height:120px;
            border-radius:50%;
            background:#fff;
            border:1px solid var(--line);
            display:grid;
            place-items:center;
            text-align:center;
        }

        .score-ring-inner strong{
            display:block;
            font-size:38px;
            line-height:1;
        }

        .score-ring-inner span{
            color:var(--muted);
            font-size:12px;
            font-weight:800;
            text-transform:uppercase;
            letter-spacing:.7px;
        }

        .verdict-badge{
            display:inline-flex;
            align-items:center;
            gap:8px;
            padding:10px 14px;
            border-radius:999px;
            color:#fff;
            font-size:13px;
            font-weight:800;
            margin-bottom:12px;
            box-shadow:0 12px 22px rgba(15,23,42,0.10);
        }

        .summary-line{
            margin:0;
            color:var(--muted);
            line-height:1.8;
            max-width:680px;
            font-size:15px;
        }

        .stats-row{
            margin-top:18px;
            display:grid;
            grid-template-columns:repeat(3, 1fr);
            gap:12px;
        }

        .stat-box{
            padding:16px;
            border-radius:16px;
            border:1px solid var(--line);
            background:#fff;
        }

        .stat-box span{
            display:block;
            color:var(--muted);
            font-size:12px;
            font-weight:800;
            text-transform:uppercase;
            letter-spacing:.7px;
            margin-bottom:8px;
        }

        .stat-box strong{
            font-size:30px;
            letter-spacing:-.9px;
        }

        .action-grid{
            display:grid;
            grid-template-columns:repeat(3, 1fr);
            gap:12px;
            margin-bottom:14px;
        }

        .action-card{
            padding:20px;
        }

        .action-pill{
            display:inline-flex;
            align-items:center;
            gap:8px;
            padding:7px 10px;
            border-radius:999px;
            background:#eff6ff;
            border:1px solid #d8e6ff;
            color:#1d4ed8;
            font-size:11px;
            font-weight:800;
            text-transform:uppercase;
            letter-spacing:.8px;
            margin-bottom:12px;
        }

        .action-card h3{
            margin:0 0 8px;
            font-size:18px;
            letter-spacing:-.4px;
        }

        .action-card p{
            margin:0 0 12px;
            color:var(--muted);
            font-size:14px;
            line-height:1.65;
        }

        .link-row{
            display:flex;
            flex-wrap:wrap;
            gap:10px;
        }

        .link-btn{
            display:inline-flex;
            align-items:center;
            gap:8px;
        }

        .ghost-tag{
            display:inline-flex;
            align-items:center;
            gap:8px;
            padding:10px 14px;
            border-radius:999px;
            background:#fff;
            border:1px solid var(--line);
            color:var(--muted);
            font-size:14px;
            font-weight:700;
        }

        .accordion{
            display:grid;
            gap:12px;
            margin-top:14px;
        }

        .accordion-item{
            background:var(--surface);
            backdrop-filter:blur(12px);
            border:1px solid rgba(216,229,243,0.82);
            border-radius:22px;
            box-shadow:var(--shadow);
            overflow:hidden;
            transition:box-shadow .2s ease, transform .2s ease;
        }

        .accordion-item:hover{
            transform:translateY(-2px);
            box-shadow:0 24px 52px rgba(37,99,235,0.10);
        }

        .accordion-item[open]{
            box-shadow:var(--shadow-lg);
        }

        .accordion-item summary{
            list-style:none;
            cursor:pointer;
            display:flex;
            align-items:center;
            justify-content:space-between;
            gap:12px;
            padding:20px 22px;
        }

        .accordion-item summary::-webkit-details-marker{
            display:none;
        }

        .acc-left{
            display:flex;
            align-items:center;
            gap:12px;
        }

        .acc-index{
            display:inline-flex;
            align-items:center;
            justify-content:center;
            min-width:44px;
            height:44px;
            border-radius:14px;
            background:#eff6ff;
            color:#1d4ed8;
            font-weight:800;
            font-size:13px;
            letter-spacing:.5px;
        }

        .acc-title{
            font-size:20px;
            font-weight:800;
            letter-spacing:-.4px;
        }

        .acc-sub{
            color:var(--muted);
            font-size:13px;
            margin-top:4px;
        }

        .acc-icon{
            width:34px;
            height:34px;
            border-radius:999px;
            display:grid;
            place-items:center;
            background:#fff;
            border:1px solid var(--line);
            color:#1d4ed8;
            font-weight:800;
            transition:transform .2s ease;
        }

        .accordion-item[open] .acc-icon{
            transform:rotate(45deg);
        }

        .acc-body{
            padding:0 22px 22px 22px;
        }

        .list{
            display:grid;
            gap:12px;
        }

        .list-item{
            display:flex;
            align-items:flex-start;
            gap:12px;
            padding:14px;
            border-radius:16px;
            background:#fff;
            border:1px solid var(--line);
        }

        .bullet{
            width:30px;
            height:30px;
            border-radius:10px;
            display:grid;
            place-items:center;
            flex-shrink:0;
            font-size:14px;
            font-weight:800;
        }

        .bullet.bad{
            background:#fef2f2;
            color:var(--red);
        }

        .bullet.good{
            background:#f0fdf4;
            color:var(--green);
        }

        .bullet.voice{
            background:#eff6ff;
            color:var(--blue);
        }

        .list-item p{
            margin:0;
            color:var(--muted);
            line-height:1.7;
        }

        .quote{
            padding:16px;
            border-radius:16px;
            background:#fff;
            border:1px solid var(--line);
            color:var(--text);
            line-height:1.75;
        }

        .alt-head{
            display:flex;
            align-items:flex-start;
            justify-content:space-between;
            gap:14px;
            flex-wrap:wrap;
            margin-bottom:14px;
        }

        .alt-head strong{
            font-size:24px;
            letter-spacing:-.6px;
        }

        .alt-head p{
            margin:8px 0 0;
            color:var(--muted);
            line-height:1.72;
            max-width:700px;
        }

        .alt-score{
            min-width:84px;
            height:84px;
            border-radius:22px;
            display:grid;
            place-items:center;
            color:#fff;
            font-size:28px;
            font-weight:800;
            background:linear-gradient(135deg, var(--green), #15803d);
            box-shadow:0 16px 30px rgba(22,163,74,0.18);
        }

        .compare-grid{
            display:grid;
            grid-template-columns:1fr 1fr;
            gap:12px;
        }

        .compare-box{
            padding:16px;
            border-radius:18px;
            background:#fff;
            border:1px solid var(--line);
        }

        .compare-box span{
            display:block;
            color:var(--muted);
            font-size:12px;
            font-weight:800;
            text-transform:uppercase;
            letter-spacing:.7px;
            margin-bottom:7px;
        }

        .compare-box strong{
            display:block;
            margin-bottom:10px;
        }

        .compact-list{
            margin:0;
            padding-left:18px;
            color:var(--muted);
            line-height:1.7;
        }

        .empty-card{
            padding:30px;
        }

        .empty-card h2{
            margin:14px 0 8px;
            font-size:32px;
            letter-spacing:-.9px;
        }

        .empty-card p{
            margin:0;
            color:var(--muted);
            line-height:1.7;
        }

        .site-footer{
            margin-top:42px;
            border-top:1px solid rgba(199,216,238,0.65);
            background:rgba(255,255,255,0.50);
            backdrop-filter:blur(10px);
        }

        .footer{
            padding:24px 0 34px;
            display:flex;
            align-items:flex-start;
            justify-content:space-between;
            gap:18px;
            color:var(--muted);
            line-height:1.7;
        }

        .footer strong{
            color:var(--text);
        }

        .footer-links{
            display:flex;
            flex-wrap:wrap;
            gap:10px 14px;
        }

        [data-reveal]{
            opacity:0;
            transform:translateY(30px) scale(.985);
            transition:opacity .75s ease, transform .75s ease;
        }

        [data-reveal].visible{
            opacity:1;
            transform:translateY(0) scale(1);
        }

        @media (max-width: 1040px){
            .hero-grid{
                grid-template-columns:1fr;
            }

            .feature-grid,
            .action-grid{
                grid-template-columns:repeat(2, 1fr);
            }

            .result-head,
            .section-head.row,
            .cta-card,
            .footer,
            .nav{
                flex-direction:column;
                align-items:flex-start;
            }
        }

        @media (max-width: 760px){
            .container{
                width:min(100% - 18px, var(--max));
            }

            .feature-grid,
            .stats-row,
            .action-grid,
            .compare-grid{
                grid-template-columns:1fr;
            }

            .search-shell,
            .inline-search{
                flex-direction:column;
                align-items:stretch;
            }

            .search-shell button,
            .inline-search button,
            .btn,
            .link-btn{
                width:100%;
                justify-content:center;
            }

            .score-wrap{
                flex-direction:column;
                align-items:flex-start;
            }

            .hero-title{
                font-size:42px;
            }

            .hero-copy{
                padding:24px 2px 24px 2px;
            }

            .hero-scene-wrap{
                height:420px;
            }

            .hero-scene{
                width:100%;
                height:400px;
            }

            .scene-core{
                width:190px;
                height:190px;
            }

            .scene-ring.ring-a{
                width:280px;
                height:280px;
            }

            .scene-ring.ring-b{
                width:320px;
                height:320px;
            }

            .scene-ring.ring-c{
                width:360px;
                height:360px;
            }

            .scene-card.card-a{
                width:180px;
                left:0;
                top:20px;
            }

            .scene-card.card-b{
                width:150px;
                right:0;
                top:70px;
            }

            .scene-card.card-c{
                width:190px;
                left:16px;
                bottom:22px;
            }

            .summary-card,
            .action-card,
            .section-card,
            .cta-card,
            .info-card,
            .empty-card{
                padding:20px;
            }

            .accordion-item summary{
                padding:18px 18px;
            }

            .acc-body{
                padding:0 18px 18px 18px;
            }
        }
    </style>
</head>
<body>
    <div class="ambient">
        <div class="blob one"></div>
        <div class="blob two"></div>
        <div class="blob three"></div>
    </div>

    <header class="site-header">
        <div class="container nav">
            <a href="{{ url_for('home') }}" class="brand">
                <div class="brand-mark">V</div>
                <div class="brand-copy">
                    VETO
                    <small>Your Final Say Before Buying</small>
                </div>
            </a>

            <nav class="nav-links">
                <a class="nav-link" href="{{ url_for('home') }}">Home</a>
                <a class="nav-link" href="{{ url_for('methodology') }}">Methodology</a>
                <a class="nav-link" href="{{ url_for('faq_page') }}">FAQ</a>
                <a class="nav-link" href="{{ url_for('about') }}">About</a>
                <a class="nav-link nav-cta" href="{{ url_for('show_result', q='Jio Fiber') }}">Try Demo</a>
            </nav>
        </div>
    </header>

    <main class="page-shell">
        {{ body|safe }}
    </main>

    <footer class="site-footer">
        <div class="container footer">
            <div>
                <strong>VETO</strong><br>
                Your Final Say Before Buying.
            </div>

            <div class="footer-links">
                <a href="{{ url_for('about') }}">About</a>
                <a href="{{ url_for('methodology') }}">Methodology</a>
                <a href="{{ url_for('privacy') }}">Privacy</a>
                <a href="{{ url_for('disclaimer') }}">Disclaimer</a>
                <a href="{{ url_for('faq_page') }}">FAQ</a>
            </div>

            <div>© {{ year }} VETO</div>
        </div>
    </footer>

    <script>
        document.addEventListener("DOMContentLoaded", function () {
            const revealItems = document.querySelectorAll("[data-reveal]");
            const observer = new IntersectionObserver((entries) => {
                entries.forEach((entry) => {
                    if (entry.isIntersecting) {
                        entry.target.classList.add("visible");
                    }
                });
            }, { threshold: 0.12 });

            revealItems.forEach((item) => observer.observe(item));

            const rings = document.querySelectorAll(".js-score-ring");
            rings.forEach((ring) => {
                const target = parseInt(ring.dataset.score || "0", 10);
                const color = ring.dataset.color || "#2563eb";
                let current = 0;
                const maxSteps = Math.max(target, 1);
                const duration = 900;
                const stepTime = duration / maxSteps;

                function paint(value) {
                    const deg = Math.max(0, Math.min(360, value * 3.6));
                    ring.style.background = "conic-gradient(" + color + " " + deg + "deg, #e2e8f0 " + deg + "deg)";
                }

                paint(0);

                function run() {
                    current += 1;
                    if (current > target) current = target;
                    paint(current);
                    if (current < target) {
                        window.setTimeout(run, stepTime);
                    }
                }

                window.setTimeout(run, 120);
            });

            const scene = document.querySelector(".hero-scene");
            const wrap = document.querySelector(".hero-scene-wrap");

            if (scene && wrap) {
                wrap.addEventListener("mousemove", function(e) {
                    const rect = wrap.getBoundingClientRect();
                    const x = ((e.clientX - rect.left) / rect.width - 0.5) * 16;
                    const y = ((e.clientY - rect.top) / rect.height - 0.5) * 16;
                    scene.style.transform = "rotateX(" + (-y) + "deg) rotateY(" + x + "deg)";
                });

                wrap.addEventListener("mouseleave", function() {
                    scene.style.transform = "rotateX(0deg) rotateY(0deg)";
                });
            }
        });
    </script>
</body>
</html>
"""

HOME_BODY_TEMPLATE = """
<section class="hero">
    <div class="container hero-grid">
        <div class="hero-copy" data-reveal>
            <span class="eyebrow">Decision engine</span>
            <h1 class="hero-title">Don't buy blind.<span class="accent">Check VETO first.</span></h1>
            <p class="hero-sub">
                Search any product or service and get a clean verdict before you spend money.
            </p>

            <form class="search-shell" action="{{ url_for('show_result') }}" method="get">
                <input type="text" name="q" placeholder="Search Jio Fiber, OYO Rooms, boAt Airdopes..." required>
                <button type="submit">Check VETO</button>
            </form>

            <div class="micro-row">
                <div class="micro-pill">📊 Trust Score</div>
                <div class="micro-pill">⚠️ Risk Signals</div>
                <div class="micro-pill">🔁 Better Choice</div>
            </div>

            <div class="micro-row">
                {% for item in trending_preview %}
                    <a class="chip" href="{{ url_for('show_result', q=item) }}">{{ item }}</a>
                {% endfor %}
            </div>
        </div>

        <div class="hero-scene-wrap" data-reveal>
            <div class="hero-scene">
                <div class="scene-ring ring-a"></div>
                <div class="scene-ring ring-b"></div>
                <div class="scene-ring ring-c"></div>

                <div class="scene-core"></div>

                <div class="orbit-dot one"></div>
                <div class="orbit-dot two"></div>
                <div class="orbit-dot three"></div>

                <div class="scene-card card-a">
                    <span class="tiny-label">Verdict layer</span>
                    <div class="scene-big">
                        <div>
                            <strong>Final call</strong>
                            <div style="color: var(--muted); font-size:14px;">Fast answer before buying</div>
                        </div>
                        <div class="scene-badge">84</div>
                    </div>
                    <div class="scene-line">Buy with <b>clarity</b>, not chaos.</div>
                </div>

                <div class="scene-card card-b">
                    <span class="tiny-label">Signal</span>
                    <div style="font-size:24px; font-weight:800; letter-spacing:-.8px; margin-bottom:6px;">Risk + Trust</div>
                    <div style="color:var(--muted); font-size:14px; line-height:1.65;">What matters most.</div>
                </div>

                <div class="scene-card card-c">
                    <span class="tiny-label">Explore faster</span>
                    <div class="scene-line">Product link</div>
                    <div class="scene-line">Review link</div>
                    <div class="scene-line">Better alternative</div>
                </div>
            </div>
        </div>
    </div>
</section>

<section class="section">
    <div class="container">
        <div class="cta-card" data-reveal>
            <div>
                <h3>Use VETO on something you're actually planning to buy.</h3>
                <p>That is where it feels most useful.</p>
            </div>
            <a class="btn" href="{{ url_for('show_result', q='Jio Fiber') }}">Open Demo</a>
        </div>
    </div>
</section>
"""

RESULT_BODY_TEMPLATE = """
<section class="section" style="padding-top:30px;">
    <div class="container">
        <a class="back-link" href="{{ url_for('home') }}">← Search another product</a>

        <div class="result-head">
            <div>
                <span class="eyebrow">Verdict</span>
                <h1 class="page-title">{{ result.name }}</h1>
                <p class="page-sub">Final call before you buy.</p>
            </div>

            <form class="inline-search" action="{{ url_for('show_result') }}" method="get">
                <input type="text" name="q" placeholder="Search another item..." required>
                <button type="submit">Search</button>
            </form>
        </div>

        {% if not has_data %}
            <div class="empty-card" data-reveal>
                <span class="eyebrow">No data yet</span>
                <h2>VETO does not have enough structured signals for this search yet.</h2>
                <p>Try one of the currently available products below.</p>

                <div class="micro-row">
                    {% for item in trending %}
                        <a class="chip" href="{{ url_for('show_result', q=item) }}">{{ item }}</a>
                    {% endfor %}
                </div>
            </div>
        {% else %}
            <div class="summary-card" data-reveal>
                <div class="score-wrap">
                    <div class="score-ring js-score-ring" data-score="{{ result.score }}" data-color="{{ result.ring_color }}" style="--ring: {{ result.ring_color }};">
                        <div class="score-ring-inner">
                            <div>
                                <strong>{{ result.score }}</strong>
                                <span>Trust score</span>
                            </div>
                        </div>
                    </div>

                    <div>
                        <div class="verdict-badge" style="background: {{ result.ring_color }};">
                            <span>{{ result.emoji }}</span>
                            <span>{{ result.verdict }}</span>
                        </div>
                        <p class="summary-line">{{ result.summary_line }}</p>
                        <p class="summary-line" style="margin-top:10px;"><strong>{{ recommendation }}</strong> — {{ next_action }}</p>
                    </div>
                </div>

                <div class="stats-row">
                    <div class="stat-box">
                        <span>Complaints</span>
                        <strong>{{ result.complaints }}</strong>
                    </div>
                    <div class="stat-box">
                        <span>Praises</span>
                        <strong>{{ result.praises }}</strong>
                    </div>
                    <div class="stat-box">
                        <span>Sources</span>
                        <strong>{{ clickable_source_count }}</strong>
                    </div>
                </div>
            </div>

            <div class="action-grid">
                <div class="action-card" data-reveal>
                    <div class="action-pill">Current product</div>
                    <h3>Open product links</h3>
                    <p>Official or main links for what you searched.</p>
                    <div class="link-row">
                        {% if result.product_links %}
                            {% for link in result.product_links %}
                                {% if link.url %}
                                    <a class="link-btn" href="{{ link.url }}" target="_blank" rel="noopener noreferrer">{{ link.label }}</a>
                                {% endif %}
                            {% endfor %}
                        {% else %}
                            <span class="ghost-tag">No product links yet</span>
                        {% endif %}
                    </div>
                </div>

                <div class="action-card" data-reveal>
                    <div class="action-pill">Reviews</div>
                    <h3>Check review links</h3>
                    <p>Review-style links if available in the current dataset.</p>
                    <div class="link-row">
                        {% if result.review_links %}
                            {% for link in result.review_links %}
                                {% if link.url %}
                                    <a class="link-btn" href="{{ link.url }}" target="_blank" rel="noopener noreferrer">{{ link.label }}</a>
                                {% endif %}
                            {% endfor %}
                        {% else %}
                            <span class="ghost-tag">Detailed review links later</span>
                        {% endif %}
                    </div>
                </div>

                <div class="action-card" data-reveal>
                    <div class="action-pill">Alternative</div>
                    <h3>Open compare option</h3>
                    <p>Jump to another option quickly if you want to compare.</p>
                    <div class="link-row">
                        {% if result.alt_links %}
                            {% for link in result.alt_links %}
                                {% if link.url %}
                                    <a class="link-btn" href="{{ link.url }}" target="_blank" rel="noopener noreferrer">{{ link.label }}</a>
                                {% endif %}
                            {% endfor %}
                        {% else %}
                            <span class="ghost-tag">No alternative links yet</span>
                        {% endif %}
                    </div>
                </div>
            </div>

            <div class="accordion">
                <details class="accordion-item" open data-reveal>
                    <summary>
                        <div class="acc-left">
                            <div class="acc-index">01</div>
                            <div>
                                <div class="acc-title">What people complain about</div>
                                <div class="acc-sub">Main downside signals</div>
                            </div>
                        </div>
                        <div class="acc-icon">+</div>
                    </summary>
                    <div class="acc-body">
                        <div class="list">
                            {% for point in result.bad_points %}
                                <div class="list-item">
                                    <div class="bullet bad">!</div>
                                    <div>
                                        <p>{{ point }}</p>
                                    </div>
                                </div>
                            {% endfor %}
                        </div>
                    </div>
                </details>

                <details class="accordion-item" data-reveal>
                    <summary>
                        <div class="acc-left">
                            <div class="acc-index">02</div>
                            <div>
                                <div class="acc-title">What people like</div>
                                <div class="acc-sub">Main upside signals</div>
                            </div>
                        </div>
                        <div class="acc-icon">+</div>
                    </summary>
                    <div class="acc-body">
                        <div class="list">
                            {% for point in result.good_points %}
                                <div class="list-item">
                                    <div class="bullet good">+</div>
                                    <div>
                                        <p>{{ point }}</p>
                                    </div>
                                </div>
                            {% endfor %}
                        </div>
                    </div>
                </details>

                <details class="accordion-item" data-reveal>
                    <summary>
                        <div class="acc-left">
                            <div class="acc-index">03</div>
                            <div>
                                <div class="acc-title">Real voice snippets</div>
                                <div class="acc-sub">Quick sentiment feel</div>
                            </div>
                        </div>
                        <div class="acc-icon">+</div>
                    </summary>
                    <div class="acc-body">
                        <div class="list">
                            {% for voice in result.voices %}
                                <div class="quote">“{{ voice }}”</div>
                            {% endfor %}
                        </div>
                    </div>
                </details>

                <details class="accordion-item" data-reveal>
                    <summary>
                        <div class="acc-left">
                            <div class="acc-index">04</div>
                            <div>
                                <div class="acc-title">{{ alt_heading }}</div>
                                <div class="acc-sub">{{ alt_subheading }}</div>
                            </div>
                        </div>
                        <div class="acc-icon">+</div>
                    </summary>
                    <div class="acc-body">
                        <div class="alt-head">
                            <div>
                                <strong>{{ result.alt_name }}</strong>
                                <p>{{ result.alt_reason }}</p>
                            </div>
                            <div class="alt-score">{{ result.alt_score }}</div>
                        </div>

                        <div class="list">
                            {% for point in result.alt_good %}
                                <div class="list-item">
                                    <div class="bullet good">+</div>
                                    <div>
                                        <p>{{ point }}</p>
                                    </div>
                                </div>
                            {% endfor %}

                            {% for point in result.alt_bad %}
                                <div class="list-item">
                                    <div class="bullet bad">!</div>
                                    <div>
                                        <p>{{ point }}</p>
                                    </div>
                                </div>
                            {% endfor %}
                        </div>

                        {% if result.alt_links %}
                            <div class="link-row" style="margin-top:14px;">
                                {% for link in result.alt_links %}
                                    {% if link.url %}
                                        <a class="link-btn" href="{{ link.url }}" target="_blank" rel="noopener noreferrer">{{ link.label }}</a>
                                    {% endif %}
                                {% endfor %}
                            </div>
                        {% endif %}
                    </div>
                </details>

                <details class="accordion-item" data-reveal>
                    <summary>
                        <div class="acc-left">
                            <div class="acc-index">05</div>
                            <div>
                                <div class="acc-title">Current vs alternative</div>
                                <div class="acc-sub">Quick comparison</div>
                            </div>
                        </div>
                        <div class="acc-icon">+</div>
                    </summary>
                    <div class="acc-body">
                        <div class="compare-grid">
                            <div class="compare-box">
                                <span>Current pick</span>
                                <strong>{{ result.name }}</strong>
                                <ul class="compact-list">
                                    {% for point in current_best %}
                                        <li><strong>Good:</strong> {{ point }}</li>
                                    {% endfor %}
                                    {% for point in current_risk %}
                                        <li><strong>Risk:</strong> {{ point }}</li>
                                    {% endfor %}
                                </ul>
                            </div>

                            <div class="compare-box">
                                <span>Alternative</span>
                                <strong>{{ result.alt_name }}</strong>
                                <ul class="compact-list">
                                    {% for point in alt_good_short %}
                                        <li><strong>Good:</strong> {{ point }}</li>
                                    {% endfor %}
                                    {% for point in alt_bad_short %}
                                        <li><strong>Risk:</strong> {{ point }}</li>
                                    {% endfor %}
                                </ul>
                            </div>
                        </div>
                    </div>
                </details>

                <details class="accordion-item" data-reveal>
                    <summary>
                        <div class="acc-left">
                            <div class="acc-index">06</div>
                            <div>
                                <div class="acc-title">Verify with public sources</div>
                                <div class="acc-sub">Open the supporting links</div>
                            </div>
                        </div>
                        <div class="acc-icon">+</div>
                    </summary>
                    <div class="acc-body">
                        <div class="link-row">
                            {% for link in result.sources %}
                                {% if link.url %}
                                    <a class="link-btn" href="{{ link.url }}" target="_blank" rel="noopener noreferrer">{{ link.label }}</a>
                                {% else %}
                                    <span class="ghost-tag">{{ link.label }}</span>
                                {% endif %}
                            {% endfor %}
                        </div>
                    </div>
                </details>
            </div>
        {% endif %}
    </div>
</section>
"""

INFO_BODY_TEMPLATE = """
<section class="section" style="padding-top:34px;">
    <div class="container">
        <div class="summary-card" data-reveal>
            <span class="eyebrow">{{ eyebrow }}</span>
            <h1 class="page-title">{{ heading }}</h1>
            <p class="page-sub" style="max-width:760px;">{{ subtitle }}</p>
        </div>

        <div class="feature-grid" style="margin-top:14px;">
            {% for card in cards %}
                <div class="info-card" data-reveal>
                    <div class="icon-box">{{ card.icon }}</div>
                    <h3>{{ card.title }}</h3>
                    <p>{{ card.text }}</p>
                </div>
            {% endfor %}
        </div>
    </div>
</section>
"""


def safe_int(value):
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


def normalize_text_list(value):
    if value is None:
        return []

    if isinstance(value, (list, tuple)):
        return [str(item) for item in value if str(item).strip()]

    text = str(value).strip()
    return [text] if text else []


def host_label(url):
    if not url:
        return "Link"

    host = urlparse(url).netloc.lower().replace("www.", "")
    if not host:
        return "Link"

    mapping = {
        "reddit.com": "Reddit",
        "amazon.in": "Amazon",
        "amazon.com": "Amazon",
        "flipkart.com": "Flipkart",
        "play.google.com": "Google Play",
        "apps.apple.com": "App Store",
        "trustpilot.com": "Trustpilot",
        "consumercomplaints.in": "Consumer Complaints",
        "youtube.com": "YouTube",
        "x.com": "X",
        "twitter.com": "X",
    }

    if host in mapping:
        return mapping[host]

    return host.split(".")[0].replace("-", " ").title()


def normalize_links(value):
    if not value:
        return []

    items = value if isinstance(value, (list, tuple)) else [value]
    cleaned = []

    for item in items:
        label = ""
        url = ""

        if isinstance(item, dict):
            label = str(
                item.get("label")
                or item.get("name")
                or item.get("title")
                or ""
            ).strip()

            url = str(
                item.get("url")
                or item.get("link")
                or item.get("href")
                or ""
            ).strip()
        else:
            text = str(item).strip()
            if text.startswith("http://") or text.startswith("https://"):
                url = text
                label = host_label(text)
            else:
                label = text

        if url and not (url.startswith("http://") or url.startswith("https://")):
            url = ""

        if not label:
            label = host_label(url) if url else "Link"

        cleaned.append({"label": label, "url": url})

    unique = []
    seen = set()

    for item in cleaned:
        key = (item["label"], item["url"])
        if key not in seen:
            seen.add(key)
            unique.append(item)

    return unique


def color_value(value):
    if not value:
        return "#2563eb"

    raw = str(value).strip().lower()

    palette = {
        "green": "#16a34a",
        "red": "#dc2626",
        "orange": "#ea580c",
        "yellow": "#ca8a04",
        "blue": "#2563eb",
        "gray": "#64748b",
    }

    if raw.startswith("#"):
        return raw

    return palette.get(raw, "#2563eb")


def get_recommendation(score, verdict):
    verdict_text = str(verdict).upper()

    if "NO DATA" in verdict_text:
        return "WAIT"

    if score >= 80:
        return "BUY"
    if score >= 60:
        return "BUY WITH CAUTION"
    if score >= 40:
        return "WAIT"
    return "AVOID"


def get_next_action(recommendation):
    actions = {
        "BUY": "Strong enough to move ahead after one quick final verification.",
        "BUY WITH CAUTION": "Looks usable, but make sure the main complaints do not affect your use case.",
        "WAIT": "Do not rush. Compare once more before making the final decision.",
        "AVOID": "Too many downside signals right now. Better to stay away.",
    }
    return actions.get(recommendation, "Compare once more before deciding.")


def get_summary_line(recommendation, good_points, bad_points):
    top_good = good_points[0] if good_points else "some positive signals"
    top_bad = bad_points[0] if bad_points else "some downside signals"

    if recommendation == "BUY":
        return f"Overall signal is strong. Main upside: {top_good}"
    if recommendation == "BUY WITH CAUTION":
        return f"Looks decent, but watch this carefully: {top_bad}"
    if recommendation == "WAIT":
        return f"Signal is mixed right now. Biggest concern: {top_bad}"
    if recommendation == "AVOID":
        return f"Downside currently outweighs confidence. Biggest issue: {top_bad}"
    return "Not enough structured data yet."


def render_page(title, body_html, description="VETO - Your Final Say Before Buying"):
    return render_template_string(
        PAGE_TEMPLATE,
        title=title,
        description=description,
        body=body_html,
        year=datetime.now().year,
    )


def render_info_page(heading, eyebrow, subtitle, cards):
    body = render_template_string(
        INFO_BODY_TEMPLATE,
        heading=heading,
        eyebrow=eyebrow,
        subtitle=subtitle,
        cards=cards,
    )
    return render_page(f"{heading} | VETO", body, subtitle)


@app.route("/")
def home():
    body = render_template_string(
        HOME_BODY_TEMPLATE,
        trending_preview=TRENDING_ITEMS[:5],
    )
    return render_page(
        "VETO | Your Final Say Before Buying",
        body,
        "Search any product or service and get a cleaner verdict before buying.",
    )


@app.route("/result")
def show_result():
    query = request.args.get("q", "").strip()

    if not query:
        return redirect(url_for("home"))

    raw = analyze(query) or {}

    score = safe_int(raw.get("score", 0))
    verdict = raw.get("verdict", "NO DATA YET")
    recommendation = get_recommendation(score, verdict)

    bad_points = normalize_text_list(raw.get("bad_points"))
    good_points = normalize_text_list(raw.get("good_points"))
    voices = normalize_text_list(raw.get("voices"))
    alt_good = normalize_text_list(raw.get("alt_good"))
    alt_bad = normalize_text_list(raw.get("alt_bad"))

    product_links = normalize_links(raw.get("product_links"))
    review_links = normalize_links(raw.get("review_links"))
    alt_links = normalize_links(raw.get("alt_links"))
    sources = normalize_links(raw.get("sources"))

    if not bad_points:
        bad_points = ["Not enough negative signals added yet."]

    if not good_points:
        good_points = ["Not enough positive signals added yet."]

    if not voices:
        voices = ["Not enough voice snippets available yet."]

    if not alt_good:
        alt_good = ["Alternative strengths will appear here as the dataset grows."]

    if not alt_bad:
        alt_bad = ["No major alternative caution point added yet."]

    if not sources:
        sources = [{"label": "Source links will appear here later.", "url": ""}]

    clickable_source_count = len([item for item in sources if item.get("url")])

    result = {
        "name": raw.get("name") or raw.get("product_name") or query,
        "score": score,
        "verdict": verdict,
        "emoji": raw.get("emoji", "🔍"),
        "ring_color": color_value(raw.get("color")),
        "complaints": safe_int(raw.get("complaints", 0)),
        "praises": safe_int(raw.get("praises", 0)),
        "bad_points": bad_points,
        "good_points": good_points,
        "voices": voices,
        "alt_name": raw.get("alt_name") or "No alternative yet",
        "alt_score": safe_int(raw.get("alt_score", 0)),
        "alt_reason": raw.get("alt_reason") or "Alternative reasoning will appear here as more structured entries are added.",
        "alt_good": alt_good,
        "alt_bad": alt_bad,
        "product_links": product_links,
        "review_links": review_links,
        "alt_links": alt_links,
        "sources": sources,
        "summary_line": get_summary_line(recommendation, good_points, bad_points),
    }

    has_data = (
        "NO DATA" not in str(verdict).upper()
        or score > 0
        or result["complaints"] > 0
        or result["praises"] > 0
    )

    alt_heading = "Better alternative" if result["alt_score"] > result["score"] else "Next option to compare"
    alt_subheading = (
        "What looks stronger right now"
        if result["alt_score"] > result["score"]
        else "Not necessarily better, but worth checking"
    )

    body = render_template_string(
        RESULT_BODY_TEMPLATE,
        result=result,
        recommendation=recommendation,
        next_action=get_next_action(recommendation),
        has_data=has_data,
        trending=TRENDING_ITEMS,
        clickable_source_count=clickable_source_count,
        current_best=good_points[:2],
        current_risk=bad_points[:2],
        alt_good_short=alt_good[:2],
        alt_bad_short=alt_bad[:2],
        alt_heading=alt_heading,
        alt_subheading=alt_subheading,
    )

    return render_page(
        f"{result['name']} Verdict | VETO",
        body,
        f"See the trust score, verdict, complaint themes, praise signals, and alternative for {result['name']}.",
    )


@app.route("/about")
def about():
    cards = [
        {
            "icon": "🎯",
            "title": "What VETO is",
            "text": "A product and service truth engine built to reduce buying confusion before you spend money.",
        },
        {
            "icon": "🧠",
            "title": "Why it exists",
            "text": "Most review platforms create noise. VETO compresses the strongest buying signals into one cleaner view.",
        },
        {
            "icon": "📌",
            "title": "What you get",
            "text": "Score, verdict, risk signals, positive signals, voice snippets, alternatives, and direct links.",
        },
    ]
    return render_info_page(
        "About VETO",
        "Company",
        "VETO exists to make pre-purchase decisions faster, cleaner, and less confusing.",
        cards,
    )


@app.route("/methodology")
def methodology():
    cards = [
        {
            "icon": "📊",
            "title": "Structured scoring",
            "text": "Scores reflect complaint weight, praise signals, verdict logic, and comparison strength in the current dataset.",
        },
        {
            "icon": "🗣️",
            "title": "Voice layer",
            "text": "Short snippets represent public-sentiment style observations so users feel the signal, not just the number.",
        },
        {
            "icon": "🔍",
            "title": "Verification matters",
            "text": "VETO helps you decide faster, but major spending decisions should still be verified through direct sources.",
        },
    ]
    return render_info_page(
        "Methodology",
        "Trust system",
        "VETO is a decision-support layer, not absolute truth.",
        cards,
    )


@app.route("/privacy")
def privacy():
    cards = [
        {
            "icon": "🔒",
            "title": "Simple usage",
            "text": "At this stage, users can search without creating an account.",
        },
        {
            "icon": "🧾",
            "title": "Lean approach",
            "text": "The platform is designed to stay useful without unnecessary friction or complexity.",
        },
        {
            "icon": "⚙️",
            "title": "Future updates",
            "text": "If data practices change later, this page will be updated clearly.",
        },
    ]
    return render_info_page(
        "Privacy",
        "User trust",
        "VETO should feel useful without feeling invasive.",
        cards,
    )


@app.route("/disclaimer")
def disclaimer():
    cards = [
        {
            "icon": "📌",
            "title": "Not absolute truth",
            "text": "VETO provides a structured decision view. It is not legal, financial, or professional advice.",
        },
        {
            "icon": "⚠️",
            "title": "Things can change",
            "text": "Service quality, pricing, and user experience can vary by place and time.",
        },
        {
            "icon": "✅",
            "title": "Use judgment too",
            "text": "Always verify important purchases before spending significant money.",
        },
    ]
    return render_info_page(
        "Disclaimer",
        "Read before use",
        "VETO helps you decide faster, but the final choice is still yours.",
        cards,
    )


@app.route("/faq")
def faq_page():
    cards = [
        {
            "icon": "❓",
            "title": "Is VETO just a review site?",
            "text": "No. It is a decision screen that compresses noisy public signals into a simpler buying view.",
        },
        {
            "icon": "🧮",
            "title": "Does a high score mean perfect?",
            "text": "No. It only means the current signals look relatively stronger than the downside.",
        },
        {
            "icon": "🚀",
            "title": "Will more products be added?",
            "text": "Yes. The database will keep expanding over time.",
        },
    ]
    return render_info_page(
        "FAQ",
        "Common questions",
        "The main things a first-time visitor should know about VETO.",
        cards,
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)