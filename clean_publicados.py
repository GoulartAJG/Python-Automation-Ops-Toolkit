import os
import argparse
from datetime import datetime, timedelta
from pathlib import Path

BASE_DIR = Path(r"F:\Publicados")
DEFAULT_DAYS = 2

PHOTO_EXTENSIONS = {".png", ".jpg", ".jpeg", ".bmp", ".gif", ".webp"}
LOG_EXTENSIONS = {".log", ".txt"}
TMP_EXTENSIONS = {".pdf", ".tmp", ".txt", ".log"}


def is_older_than(file_path: Path, cutoff: datetime) -> bool:
    mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
    return mtime < cutoff


def matches_log_folder(folder: Path) -> bool:
    return folder.name.lower() == "log"


def matches_fotos_folder(folder: Path) -> bool:
    parts = [p.lower() for p in folder.parts]
    return folder.name.lower() == "fotos" and "mobile" in parts and "touch" in parts


def matches_tmp_folder(folder: Path) -> bool:
    parts = [p.lower() for p in folder.parts]
    return folder.name.lower() == "tmp" and "aniel.connect" in parts


def should_delete_in_folder(file_path: Path, folder: Path) -> bool:
    suffix = file_path.suffix.lower()

    if matches_fotos_folder(folder):
        return suffix in PHOTO_EXTENSIONS

    if matches_log_folder(folder):
        return True

    if matches_tmp_folder(folder):
        return suffix in TMP_EXTENSIONS or suffix != ""

    return False


def process_folder(folder: Path, cutoff: datetime, dry_run: bool, report_lines: list[str]) -> tuple[int, int]:
    deleted = 0
    failed = 0

    for entry in folder.iterdir():
        if not entry.is_file():
            continue

        if not should_delete_in_folder(entry, folder):
            continue

        try:
            if is_older_than(entry, cutoff):
                action = "[SIMULAÇÃO] Remover" if dry_run else "Removido"
                size_kb = round(entry.stat().st_size / 1024, 2)
                report_lines.append(f"{action}: {entry} | {size_kb} KB")
                if not dry_run:
                    entry.unlink()
                deleted += 1
        except Exception as exc:
            report_lines.append(f"[ERRO] {entry} | {exc}")
            failed += 1

    return deleted, failed


def find_target_folders(base_dir: Path) -> list[Path]:
    targets = []
    for root, dirs, files in os.walk(base_dir):
        folder = Path(root)
        if matches_fotos_folder(folder) or matches_log_folder(folder) or matches_tmp_folder(folder):
            targets.append(folder)
    return sorted(set(targets))


def write_log(log_file: Path | None, lines: list[str]) -> None:
    if not log_file:
        return
    log_file.parent.mkdir(parents=True, exist_ok=True)
    with log_file.open("a", encoding="utf-8") as f:
        f.write("\n" + "=" * 80 + "\n")
        f.write(f"Execução: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n")
        f.write("\n".join(lines))
        f.write("\n")


def main() -> None:
    parser = argparse.ArgumentParser(description="Limpeza automática de fotos, logs e arquivos temporários em F:\\Publicados")
    parser.add_argument("--days", type=int, default=DEFAULT_DAYS, help="Quantidade de dias a manter. Padrão: 2")
    parser.add_argument("--dry-run", action="store_true", help="Somente simula, sem apagar arquivos")
    parser.add_argument("--log-file", type=Path, help=r"Caminho do arquivo de log. Exemplo: C:\Scripts\Logs\limpeza.log")
    args = parser.parse_args()

    cutoff = datetime.now() - timedelta(days=args.days)

    report_lines: list[str] = []
    report_lines.append(f"Pasta base: {BASE_DIR}")
    report_lines.append(f"Manter arquivos dos últimos {args.days} dia(s)")
    report_lines.append(f"Data limite: {cutoff.strftime('%d/%m/%Y %H:%M:%S')}")
    report_lines.append(f"Modo simulação: {'SIM' if args.dry_run else 'NÃO'}")

    if not BASE_DIR.exists():
        report_lines.append(f"[ERRO] Pasta base não encontrada: {BASE_DIR}")
        print("\n".join(report_lines))
        write_log(args.log_file, report_lines)
        return

    target_folders = find_target_folders(BASE_DIR)
    report_lines.append(f"Pastas encontradas para análise: {len(target_folders)}")

    total_deleted = 0
    total_failed = 0

    for folder in target_folders:
        report_lines.append(f"\nAnalisando pasta: {folder}")
        deleted, failed = process_folder(folder, cutoff, args.dry_run, report_lines)
        total_deleted += deleted
        total_failed += failed
        report_lines.append(f"Resumo da pasta: removidos={deleted} | erros={failed}")

    report_lines.append("\nResumo final")
    report_lines.append(f"Arquivos removidos: {total_deleted}")
    report_lines.append(f"Erros: {total_failed}")

    output = "\n".join(report_lines)
    print(output)
    write_log(args.log_file, report_lines)


if __name__ == "__main__":
    main()
