def parse_mitre_file():
    pass


if __name__ == '__main__':
    parse_mitre_file()

    lokibot = {"description": "Enterprise techniques used by Lokibot, ATT&CK software S0447 v1.0",
               "name": "Lokibot (S0447)", "domain": "mitre-enterprise", "version": "3.0",
               "techniques": [{"techniqueID": "T1071", "showSubtechniques": true},
                              {"score": 1, "techniqueID": "T1071.001", "showSubtechniques": true,
                               "comment": "Lokibot has used HTTP for C2 communications.[1]"},
                              {"score": 1, "techniqueID": "T1555", "showSubtechniques": true,
                               "comment": "Lokibot has stolen credentials from multiple applications and data sources including Windows OS credentials, email clients, FTP, and SFTP clients.[1]"},
                              {"score": 1, "techniqueID": "T1555.003", "showSubtechniques": true,
                               "comment": "Lokibot has demonstrated the ability to steal credentials from multiple applications and data sources including Safari and the Chromium and Mozilla Firefox-based web browsers.[1]"},
                              {"score": 1, "techniqueID": "T1041", "showSubtechniques": false,
                               "comment": "Lokibot has the ability to initiate contact with command and control (C2) to exfiltrate stolen data.[4]"},
                              {"techniqueID": "T1564", "showSubtechniques": true},
                              {"score": 1, "techniqueID": "T1564.001", "showSubtechniques": true,
                               "comment": "Lokibot has the ability to copy itself to a hidden file and directory.[1]"},
                              {"techniqueID": "T1056", "showSubtechniques": true},
                              {"score": 1, "techniqueID": "T1056.001", "showSubtechniques": true,
                               "comment": "Lokibot has the ability to capture input on the compromised host via keylogging.[4]"},
                              {"score": 1, "techniqueID": "T1027", "showSubtechniques": true,
                               "comment": "Lokibot has obfuscated strings with base64 encoding.[1]"},
                              {"score": 1, "techniqueID": "T1027.002", "showSubtechniques": true,
                               "comment": "Lokibot has used several packing methods for obfuscation.[1]"},
                              {"techniqueID": "T1055", "showSubtechniques": true},
                              {"score": 1, "techniqueID": "T1055.012", "showSubtechniques": true,
                               "comment": "Lokibot has used process hollowing to inject into legitimate Windows process vbc.exe.[1]"},
                              {"score": 1, "techniqueID": "T1082", "showSubtechniques": false,
                               "comment": "Lokibot has the ability to discover the computer name and Windows product name/version.[4]"},
                              {"score": 1, "techniqueID": "T1016", "showSubtechniques": false,
                               "comment": "Lokibot has the ability to discover the domain name of the infected host.[4]"},
                              {"score": 1, "techniqueID": "T1033", "showSubtechniques": false,
                               "comment": "Lokibot has the ability to discover the username on the infected host.[4]"},
                              {"techniqueID": "T1204", "showSubtechniques": true},
                              {"score": 1, "techniqueID": "T1204.002", "showSubtechniques": true,
                               "comment": "Lokibot has been executed through malicious documents contained in spearphishing e-mails.[3]"}],
               "gradient": {"colors": ["#ffffff", "#66b1ff"], "minValue": 0, "maxValue": 1},
               "legendItems": [{"label": "used by Lokibot", "color": "#66b1ff"}]}
