import customtkinter as ctk
import threading
import sys
import os
import time
from modules import recon, scanner, intel, dorking

# --- THEME CONFIGURATION ---
ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("dark-blue")

# Palette
COL_BG = "#0f172a"       
COL_PANEL = "#1e293b"    
COL_ACCENT = "#3b82f6"   # Blue
COL_STOP = "#ef4444"     # Red (Stop Button)
COL_HIGH = "#ef4444"     
COL_MED = "#f59e0b"      
COL_SAFE = "#10b981"     
COL_TEXT_MAIN = "#f1f5f9"
COL_TEXT_SUB = "#94a3b8"
COL_TERM_BG = "#020617"  

class StatCard(ctk.CTkFrame):
    def __init__(self, parent, title, icon, icon_color):
        super().__init__(parent, fg_color=COL_PANEL, corner_radius=12, border_width=0)
        self.val_var = ctk.StringVar(value="0")
        
        icon_lbl = ctk.CTkLabel(self, text=icon, font=("Segoe UI Emoji", 28), text_color=icon_color)
        icon_lbl.pack(side="left", padx=(20, 15), pady=15)
        
        data_frame = ctk.CTkFrame(self, fg_color="transparent")
        data_frame.pack(side="left", pady=10)
        
        ctk.CTkLabel(data_frame, text=title, text_color=COL_TEXT_SUB, font=("DIN", 11, "bold")).pack(anchor="w")
        ctk.CTkLabel(data_frame, textvariable=self.val_var, text_color=COL_TEXT_MAIN, font=("DIN", 24, "bold")).pack(anchor="w")
        
    def set(self, val): self.val_var.set(str(val))
    def get(self): return int(self.val_var.get()) # <--- THIS WAS MISSING

class AssetCard(ctk.CTkFrame):
    def __init__(self, parent, ip, services):
        super().__init__(parent, fg_color=COL_PANEL, corner_radius=8, border_color="#334155", border_width=1)
        self.pack(fill="x", pady=4, padx=2)
        
        header = ctk.CTkFrame(self, fg_color="transparent")
        header.pack(fill="x", padx=10, pady=8)
        
        ctk.CTkLabel(header, text="● ONLINE", text_color=COL_SAFE, font=("Arial", 10, "bold")).pack(side="left")
        ctk.CTkLabel(header, text=ip, text_color=COL_TEXT_MAIN, font=("Consolas", 14, "bold")).pack(side="left", padx=10)
        
        ports_frame = ctk.CTkFrame(self, fg_color="transparent")
        ports_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        ctk.CTkLabel(ports_frame, text="OPEN PORTS:", text_color=COL_TEXT_SUB, font=("Arial", 9, "bold")).pack(anchor="w", pady=(0,5))
        
        for svc in services:
            p_txt = f"{svc['port']} | {svc['service'][:10]}"
            badge = ctk.CTkLabel(ports_frame, text=p_txt, fg_color=COL_ACCENT, text_color="white", 
                                 corner_radius=6, font=("Consolas", 10, "bold"), padx=8, pady=2)
            badge.pack(side="left", padx=(0, 5))

class VulnCard(ctk.CTkFrame):
    def __init__(self, parent, title, severity, summary, context):
        border_col = COL_HIGH if severity >= 7.0 else (COL_MED if severity >= 4.0 else COL_SAFE)
        super().__init__(parent, fg_color=COL_PANEL, corner_radius=8, border_color=border_col, border_width=1)
        self.pack(fill="x", pady=5, padx=2)
        
        top = ctk.CTkFrame(self, fg_color="transparent")
        top.pack(fill="x", padx=12, pady=(10, 5))
        
        ctk.CTkLabel(top, text=title, text_color=border_col, font=("Arial", 13, "bold")).pack(side="left")
        
        pill = ctk.CTkLabel(top, text=f"RISK {severity}", fg_color=border_col, text_color="white",
                            corner_radius=10, font=("Arial", 10, "bold"), height=20, width=60)
        pill.pack(side="right")
        
        ctx = ctk.CTkLabel(self, text=context, text_color=COL_TEXT_SUB, font=("Consolas", 11), anchor="w")
        ctx.pack(fill="x", padx=12, pady=(0, 5))
        
        desc = ctk.CTkLabel(self, text=summary, text_color="#cbd5e1", font=("Arial", 11), 
                            anchor="w", justify="left", wraplength=480)
        desc.pack(fill="x", padx=12, pady=(0, 12))

class ASM_App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("ASM PRO | Attack Surface Manager")
        self.geometry("1300x850")
        self.configure(fg_color=COL_BG)

        # STATE MANAGEMENT
        self.scanning = False
        self.stop_event = threading.Event()

        # Layout
        self.grid_columnconfigure((0, 1, 2, 3), weight=1)
        self.grid_rowconfigure(2, weight=10)
        self.grid_rowconfigure(3, weight=1)

        # Header
        self.head = ctk.CTkFrame(self, fg_color="transparent")
        self.head.grid(row=0, column=0, columnspan=4, sticky="ew", padx=20, pady=20)
        ctk.CTkLabel(self.head, text="🚀 ASM PRO", font=("Arial", 24, "bold"), text_color="white").pack(side="left")
        
        # TOGGLE BUTTON
        self.btn = ctk.CTkButton(self.head, text="START SCAN", fg_color=COL_ACCENT, hover_color="#2563eb", 
                                 font=("Arial", 12, "bold"), width=140, height=35, command=self.toggle_scan)
        self.btn.pack(side="right")
        
        self.entry = ctk.CTkEntry(self.head, placeholder_text="Enter Target (e.g., demo.testfire.net)", 
                                  width=400, height=35, fg_color=COL_PANEL, border_width=0, text_color="white")
        self.entry.pack(side="right", padx=15)

        # Stats
        self.stat_hosts = StatCard(self, "HOSTS UP", "🌐", COL_ACCENT)
        self.stat_hosts.grid(row=1, column=0, padx=10, sticky="ew")
        self.stat_ports = StatCard(self, "SERVICES", "🔌", COL_SAFE)
        self.stat_ports.grid(row=1, column=1, padx=10, sticky="ew")
        self.stat_vulns = StatCard(self, "THREATS", "🛡️", COL_MED)
        self.stat_vulns.grid(row=1, column=2, padx=10, sticky="ew")
        self.stat_high = StatCard(self, "CRITICAL", "🔥", COL_HIGH)
        self.stat_high.grid(row=1, column=3, padx=10, sticky="ew")

        # Main Content
        self.main = ctk.CTkFrame(self, fg_color="transparent")
        self.main.grid(row=2, column=0, columnspan=4, sticky="nsew", padx=10, pady=10)
        self.main.columnconfigure(0, weight=4) 
        self.main.columnconfigure(1, weight=5) 

        self.f_left = ctk.CTkFrame(self.main, fg_color=COL_PANEL, corner_radius=12)
        self.f_left.grid(row=0, column=0, sticky="nsew", padx=5)
        ctk.CTkLabel(self.f_left, text="LIVE NETWORK ASSETS", text_color=COL_TEXT_SUB, font=("Arial", 11, "bold")).pack(anchor="w", padx=15, pady=15)
        self.scroll_assets = ctk.CTkScrollableFrame(self.f_left, fg_color="transparent")
        self.scroll_assets.pack(fill="both", expand=True, padx=5, pady=5)

        self.f_right = ctk.CTkFrame(self.main, fg_color=COL_PANEL, corner_radius=12)
        self.f_right.grid(row=0, column=1, sticky="nsew", padx=5)
        ctk.CTkLabel(self.f_right, text="VULNERABILITY INTELLIGENCE", text_color=COL_TEXT_SUB, font=("Arial", 11, "bold")).pack(anchor="w", padx=15, pady=15)
        self.scroll_vulns = ctk.CTkScrollableFrame(self.f_right, fg_color="transparent")
        self.scroll_vulns.pack(fill="both", expand=True, padx=5, pady=5)

        # Terminal
        self.term_frame = ctk.CTkFrame(self, fg_color=COL_TERM_BG, corner_radius=10, border_width=1, border_color="#334155")
        self.term_frame.grid(row=3, column=0, columnspan=4, sticky="nsew", padx=15, pady=(5, 15))
        ctk.CTkLabel(self.term_frame, text=" SYSTEM CONSOLE", font=("Consolas", 10, "bold"), text_color=COL_TEXT_SUB).pack(anchor="w", padx=5, pady=2)
        self.console = ctk.CTkTextbox(self.term_frame, fg_color="transparent", text_color="#22c55e", font=("Consolas", 11), wrap="word")
        self.console.pack(fill="both", expand=True, padx=5, pady=0)
        self.log("ASM Pro System v3.1 (Fix Applied) Loaded...")
        self.log("Ready.")

    def log(self, msg):
        timestamp = time.strftime("[%H:%M:%S]")
        self.console.insert("end", f"{timestamp} {msg}\n")
        self.console.see("end")

    def add_asset_card(self, ip, services):
        AssetCard(self.scroll_assets, ip, services)

    def add_vuln_card(self, title, severity, summary, context):
        VulnCard(self.scroll_vulns, title, severity, summary, context)

    # --- STATE CONTROL ---
    def toggle_scan(self):
        if not self.scanning:
            # START NEW SCAN
            target = self.entry.get()
            if not target:
                self.log("ERROR: Input target domain.")
                return
            
            self.scanning = True
            self.stop_event.clear() # Reset stop flag
            
            # Change Button to Stop
            self.btn.configure(text="STOP SCAN", fg_color=COL_STOP, hover_color="#c0392b")
            self.entry.configure(state="disabled")
            
            # Clear UI for new run
            self.log("="*40)
            self.log(f"INITIALIZING NEW JOB: {target}")
            for w in self.scroll_assets.winfo_children(): w.destroy()
            for w in self.scroll_vulns.winfo_children(): w.destroy()
            self.stat_hosts.set(0); self.stat_ports.set(0); self.stat_vulns.set(0); self.stat_high.set(0)
            
            # Start Thread
            threading.Thread(target=self.run_scan_logic, args=(target,), daemon=True).start()
        
        else:
            # STOP CURRENT SCAN
            self.log("[!] STOP COMMAND RECEIVED. Terminating threads...")
            self.stop_event.set() # Signal threads to stop
            self.btn.configure(text="STOPPING...", state="disabled")

    def reset_ui_state(self):
        """Called when scan finishes or is stopped"""
        self.scanning = False
        self.btn.configure(text="START SCAN", fg_color=COL_ACCENT, hover_color="#2563eb", state="normal")
        self.entry.configure(state="normal")
        self.log("Job finished/stopped. Ready for next target.")

    def run_scan_logic(self, raw_target):
        try:
            target = recon.sanitize_target(raw_target)
            self.after(0, self.log, f"Target sanitized: {target}")
            
            # CHECK STOP
            if self.stop_event.is_set(): 
                self.after(0, self.reset_ui_state)
                return

            # --- PHASE 1: DORKING ---
            self.after(0, self.log, "Phase 1: Google Dorking...")
            dorks_found = dorking.run_dorks(target)
            
            # CHECK STOP
            if self.stop_event.is_set(): 
                self.after(0, self.reset_ui_state)
                return

            if dorks_found:
                self.after(0, self.stat_vulns.set, self.stat_vulns.get() + len(dorks_found))
                for d in dorks_found:
                    sev = 9.0 if "Backup" in d['type'] or "SQL" in d['type'] else 7.5
                    if sev >= 7.0: self.after(0, self.stat_high.set, self.stat_high.get() + 1)
                    self.after(0, self.add_vuln_card, d['type'], sev, d['description'], f"Source: Google | {d['url']}")

            # --- PHASE 2: RECON ---
            self.after(0, self.log, "Phase 2: Subdomain Enumeration...")
            subs = recon.get_subdomains(target)
            if "vulnweb" in target or "testfire" in target: subs = [target]
            self.after(0, self.stat_hosts.set, len(subs))

            # --- PHASE 3: SCANNING ---
            for sub in subs:
                # CHECK STOP (Inside loop for faster stopping)
                if self.stop_event.is_set(): break
                
                ip = recon.resolve_ip(sub)
                if not ip: continue
                
                self.after(0, self.log, f"Scanning {sub} ({ip})...")
                services = scanner.scan_host(ip)
                
                if services:
                    self.after(0, self.stat_ports.set, self.stat_ports.get() + len(services))
                    self.after(0, self.add_asset_card, ip, services)
                    
                    for svc in services:
                        name = svc['service']
                        ver = svc['version']
                        cves = intel.get_vulns(name, ver)
                        
                        if cves:
                            self.after(0, self.stat_vulns.set, self.stat_vulns.get() + len(cves))
                            for c in cves:
                                sev = float(c.get('cvss', 5.0))
                                if sev >= 7.0: self.after(0, self.stat_high.set, self.stat_high.get() + 1)
                                self.after(0, self.add_vuln_card, c['id'], sev, c['summary'], f"Service: {name}")

            self.after(0, self.log, "Scan Sequence Complete.")

        except Exception as e:
            self.after(0, self.log, f"FATAL ERROR: {e}")
        finally:
            self.after(0, self.reset_ui_state)

if __name__ == "__main__":
    app = ASM_App()
    app.mainloop()