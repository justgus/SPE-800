import Foundation
import PDFKit
import AppKit
// Usage: swift mbsInspectPDF.swift PDF RENDER_DIRECTORY REPORT_JSON
let args = CommandLine.arguments
let output = URL(fileURLWithPath: args[2], isDirectory: true)
try FileManager.default.createDirectory(at: output, withIntermediateDirectories: true)
guard let doc = PDFDocument(url: URL(fileURLWithPath: args[1])) else { fatalError("Cannot open PDF") }
func png(_ image: NSImage, _ name: String) throws {
    let bitmap = NSBitmapImageRep(data: image.tiffRepresentation!)!
    try bitmap.representation(using: .png, properties: [:])!.write(to: output.appendingPathComponent(name))
}
var internalLinks = 0, externalLinks = 0, unresolvedLinks = 0
var selected: [Int] = []
var text = ""
for i in 0..<doc.pageCount {
    let page = doc.page(at:i)!, content = page.string ?? ""
    text += "\n=== PDF PAGE \(i+1), LABEL \(page.label ?? "") ===\n" + content
    for a in page.annotations where a.type == "Link" {
        if let d = a.destination, let target = d.page, doc.index(for:target) != NSNotFound { internalLinks += 1 }
        else if let action = a.action as? PDFActionGoTo, let target = action.destination.page, doc.index(for:target) != NSNotFound { internalLinks += 1 }
        else if a.url != nil || a.action is PDFActionURL { externalLinks += 1 }
        else { unresolvedLinks += 1 }
    }
    if [14,16,33,72,96,97].contains(i) || i == 0 || (i >= 12 && (i < 47 || content.contains("Figure ") || content.contains("Instantiation Review") || content.contains("Project Document History") || content.contains("Glossary"))) {
        try png(page.thumbnail(of:NSSize(width:1200,height:1600),for:.mediaBox),String(format:"mbsPage%03d.png",i+1)); selected.append(i+1)
    }
}
for start in stride(from:0,to:doc.pageCount,by:16) {
    let canvas = NSImage(size:NSSize(width:1600,height:2240)); canvas.lockFocus()
    NSColor.white.setFill(); NSRect(x:0,y:0,width:1600,height:2240).fill()
    for slot in 0..<min(16,doc.pageCount-start) {
        let page = doc.page(at:start+slot)!, x = CGFloat(slot%4)*400, y = CGFloat(3-slot/4)*560
        page.thumbnail(of:NSSize(width:380,height:525),for:.mediaBox).draw(in:NSRect(x:x+10,y:y+25,width:380,height:525))
        ("PDF \(start+slot+1) / \(page.label ?? "")" as NSString).draw(at:NSPoint(x:x+15,y:y+6),withAttributes:[.font:NSFont.systemFont(ofSize:14),.foregroundColor:NSColor.black])
    }
    canvas.unlockFocus(); try png(canvas,String(format:"mbsContact%02d.png",start/16+1))
}
try text.write(to:output.appendingPathComponent("mbsPDFText.txt"),atomically:true,encoding:.utf8)
let report: [String:Any] = ["pdf":URL(fileURLWithPath:args[1]).lastPathComponent,"pages":doc.pageCount,"internal_links_resolved":internalLinks,"external_links":externalLinks,"unresolved_link_annotations":unresolvedLinks,"rendered_all_pages_as_contact_sheets":true,"selected_page_renders":selected,"note":"Rendering and automated link checks require separate visual inspection; no human acceptance implied."]
try JSONSerialization.data(withJSONObject:report,options:[.prettyPrinted,.sortedKeys]).write(to:URL(fileURLWithPath:args[3]))
print("Rendered \(doc.pageCount) pages; resolved internal links \(internalLinks), external \(externalLinks), unresolved \(unresolvedLinks).")
