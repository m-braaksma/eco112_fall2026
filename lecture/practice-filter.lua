-- Practice-problem solutions: wrap in <details> for HTML (collapsible),
-- drop entirely for PDF (so students get a blank worksheet).
function Div(div)
  if div.classes:includes("solution-only") then
    if quarto.doc.is_format("pdf") then
      return {}
    else
      local opening = pandoc.RawBlock("html", "<details>\n<summary>Show Answer</summary>\n")
      local closing = pandoc.RawBlock("html", "</details>")
      local blocks = { opening }
      for _, b in ipairs(div.content) do
        table.insert(blocks, b)
      end
      table.insert(blocks, closing)
      return blocks
    end
  end
  return div
end

-- Track whether we're currently inside the Warm-Up section, so its lists
-- (short, one-word answers) get less blank space than full problems.
local in_warmup = false
function Header(el)
  if el.level == 2 then
    in_warmup = pandoc.utils.stringify(el):match("Warm%-Up") ~= nil
  end
  return el
end

-- On the PDF worksheet, leave blank space after each lettered sub-question
-- (a, b, c, ...) so students have room to write their work.
function OrderedList(el)
  if not quarto.doc.is_format("pdf") then
    return el
  end
  local space = in_warmup and "0.3in" or "0.9in"
  local vspace = pandoc.RawBlock("latex", "\\vspace{" .. space .. "}")
  for _, item in ipairs(el.content) do
    table.insert(item, vspace)
  end
  return el
end
