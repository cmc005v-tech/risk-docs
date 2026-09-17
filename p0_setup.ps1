# P0 内容标准化执行脚本
$base = "g:\A工作中心\风险处置Commercial risk management"

# P0-1: 确认 7 目录已存在
$dirs = @(
    "01_认知理论",
    "02_学习规划",
    "03_实操模板",
    "04_评估工具",
    "05_法规参考",
    "06_岗位认知方法论",
    "07_网站源码"
)
foreach ($d in $dirs) {
    $p = Join-Path $base $d
    if (!(Test-Path $p)) {
        New-Item -ItemType Directory -Path $p -Force | Out-Null
        Write-Host "[P0-1] Created: $d"
    } else {
        Write-Host "[P0-1] Exists: $d"
    }
}

# P0-2/3: 文件归类移动 + 统一命名
$moves = @(
    @{ Src = "1.危机应对的道与术_读书报告.docx"; Dst = "01_认知理论\读书报告《危机应对的道与术》.docx" },
    @{ Src = "2.掘金_不良资产经营_读书报告.docx"; Dst = "01_认知理论\读书报告《掘金》.docx" },
    @{ Src = "3.重大决策社会稳定风险评估指南_读书报告.docx"; Dst = "01_认知理论\读书报告《稳评指南》.docx" },
    @{ Src = "4.黑天鹅_读书报告.docx"; Dst = "01_认知理论\读书报告《黑天鹅》.docx" },
    @{ Src = "5.闪电战_AI时代上市公司舆情攻防实战手册_读书报告.docx"; Dst = "01_认知理论\读书报告《闪电战》.docx" },
    @{ Src = "6.商业风控 企业的隐形数字资产白皮书.docx"; Dst = "01_认知理论\商业风控白皮书.docx" },
    @{ Src = "投资人尽调选项目团队的五项标准.docx"; Dst = "01_认知理论\投资人五大标准.docx" },
    @{ Src = "风险处置学习方案（学习计划+书单+全套模板）.docx"; Dst = "02_学习规划\风险处置学习方案.docx" },
    @{ Src = "标准风险处置方案模板_三套预案版.docx"; Dst = "03_实操模板\模板-风险处置方案.docx" },
    @{ Src = "企业风险排查的风险评估报告模板.docx"; Dst = "03_实操模板\模板-风险评估报告.docx" },
    @{ Src = "项目结案复盘报告模板.docx"; Dst = "03_实操模板\模板-结案复盘报告.docx" },
    @{ Src = "风险隔离与止损操作SOP.docx"; Dst = "03_实操模板\模板-隔离止损SOP.docx" },
    @{ Src = "谈判沟通话术.docx"; Dst = "03_实操模板\模板-谈判话术框架.docx" },
    @{ Src = "企业风险全面尽调清单.xlsx"; Dst = "04_评估工具\工具-风险尽调清单.xlsx" },
    @{ Src = "风险损失测算模板.xlsx"; Dst = "04_评估工具\工具-损失测算.xlsx" },
    @{ Src = "风险等级评估表.xlsx"; Dst = "04_评估工具\工具-风险等级评估.xlsx" },
    @{ Src = "中央企业应急管理办法（征求意见稿）.pdf"; Dst = "05_法规参考\法规-央企应急管理办法.pdf" },
    @{ Src = "最高人民法院关于适用《中华人民共和国民法典》关干担保制度的解释 - 中华人民共和国最高人民法院.pdf"; Dst = "05_法规参考\法规-民法典担保制度解释.pdf" }
)

foreach ($m in $moves) {
    $srcPath = Join-Path $base $m.Src
    $dstPath = Join-Path $base $m.Dst
    if (Test-Path $srcPath) {
        Move-Item -Path $srcPath -Destination $dstPath -Force
        Write-Host "[P0-2] Moved: $($m.Src) -> $($m.Dst)"
    } else {
        Write-Host "[P0-2] NOT FOUND: $($m.Src)" -ForegroundColor Yellow
    }
}

# Check for 商业风险处置顾问.md
$advisorFile = Join-Path $base "商业风险处置顾问.md"
if (Test-Path $advisorFile) {
    $dstPath = Join-Path $base "06_岗位认知方法论\商业风险处置顾问.md"
    Move-Item -Path $advisorFile -Destination $dstPath -Force
    Write-Host "[P0-2] Moved: 商业风险处置顾问.md -> 06_岗位认知方法论\"
} else {
    Write-Host "[P0-2] 商业风险处置顾问.md not found in root (may not exist)" -ForegroundColor Yellow
}

# P0-4: 移动 risk-learning-site 到 07_网站源码
$siteSrc = Join-Path $base "risk-learning-site"
$siteDst = Join-Path $base "07_网站源码\risk-learning-site"
if (Test-Path $siteSrc) {
    if (Test-Path $siteDst) {
        Remove-Item -Path $siteDst -Recurse -Force
    }
    Move-Item -Path $siteSrc -Destination $siteDst -Force
    Write-Host "[P0-4] Moved: risk-learning-site -> 07_网站源码\"
} else {
    Write-Host "[P0-4] risk-learning-site not found" -ForegroundColor Yellow
}

# P0-5: 创建 assets 目录 + 复制 xlsx
$assetsDir = Join-Path $base "07_网站源码\risk-learning-site\assets"
if (!(Test-Path $assetsDir)) {
    New-Item -ItemType Directory -Path $assetsDir -Force | Out-Null
    Write-Host "[P0-5] Created: assets/"
}
$xlsxFiles = @(
    @{ Src = "04_评估工具\工具-风险尽调清单.xlsx"; Name = "工具-风险尽调清单.xlsx" },
    @{ Src = "04_评估工具\工具-损失测算.xlsx"; Name = "工具-损失测算.xlsx" },
    @{ Src = "04_评估工具\工具-风险等级评估.xlsx"; Name = "工具-风险等级评估.xlsx" }
)
foreach ($x in $xlsxFiles) {
    $srcPath = Join-Path $base $x.Src
    $dstPath = Join-Path $assetsDir $x.Name
    if (Test-Path $srcPath) {
        Copy-Item -Path $srcPath -Destination $dstPath -Force
        Write-Host "[P0-5] Copied: $($x.Name) -> assets/"
    }
}

Write-Host "`n=== P0 Execution Complete ===" -ForegroundColor Green
Write-Host "Verifying directory structure..."

# Verify
foreach ($d in $dirs) {
    $p = Join-Path $base $d
    $count = (Get-ChildItem -Path $p -File -Recurse -ErrorAction SilentlyContinue | Measure-Object).Count
    Write-Host "  $d : $count files"
}
