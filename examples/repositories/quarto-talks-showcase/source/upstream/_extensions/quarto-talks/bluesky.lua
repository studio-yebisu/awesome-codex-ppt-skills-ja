local settings = {
  enabled = false,
  max_width = 600,
}
local enhancement_included = false

local function stringify(value)
  if value == nil then
    return nil
  end

  return pandoc.utils.stringify(value)
end

local function read_boolean(value, fallback)
  if type(value) == "boolean" then
    return value
  end

  local text = stringify(value)
  if text == "true" then
    return true
  end
  if text == "false" then
    return false
  end

  return fallback
end

local function configure(meta)
  local bluesky = meta.bluesky
  if bluesky == nil then
    return meta
  end

  if type(bluesky) == "boolean" then
    settings.enabled = bluesky
    return meta
  end

  settings.enabled = read_boolean(bluesky.enabled, false)

  local requested_width = tonumber(stringify(bluesky["max-width"]))
  if requested_width ~= nil then
    settings.max_width = math.max(220, math.min(600, math.floor(requested_width)))
  end

  return meta
end

local function find_post_url(div)
  local supplied = div.attributes.url or stringify(div)
  if supplied == nil then
    return nil
  end

  return supplied:match("https://bsky%.app/profile/[A-Za-z0-9:._%%-]+/post/[A-Za-z0-9]+")
end

local function append_style(div, declaration)
  local style = div.attributes.style or ""
  if style ~= "" and not style:match(";%s*$") then
    style = style .. ";"
  end
  div.attributes.style = style .. declaration
end

local function fallback_content(url)
  return {
    pandoc.Div({
      pandoc.Para({
        pandoc.Span("Bluesky post", pandoc.Attr("", { "bluesky-kicker" })),
      }),
      pandoc.Para({
        pandoc.Link("Open post on Bluesky", url),
      }),
      pandoc.Para({
        pandoc.Span(
          "The live preview loads when this presentation is online.",
          pandoc.Attr("", { "bluesky-fallback-note" })
        ),
      }),
    }, pandoc.Attr("", { "bluesky-fallback" })),
  }
end

local function invalid_content()
  return {
    pandoc.Div({
      pandoc.Para({
        pandoc.Span("Bluesky post", pandoc.Attr("", { "bluesky-kicker" })),
      }),
      pandoc.Para({
        pandoc.Span(
          "Add a full https://bsky.app/profile/.../post/... URL.",
          pandoc.Attr("", { "bluesky-fallback-note" })
        ),
      }),
    }, pandoc.Attr("", { "bluesky-fallback" })),
  }
end

local function bluesky_post(div)
  if not div.classes:includes("bluesky-post") then
    return nil
  end

  append_style(div, "--qt-bluesky-width: " .. settings.max_width .. "px;")
  div.attributes["data-bluesky-enabled"] = settings.enabled and "true" or "false"
  div.attributes["data-bluesky-max-width"] = tostring(settings.max_width)
  div.attributes["data-bluesky-state"] = "fallback"
  div.attributes.role = "group"
  div.attributes["aria-label"] = "Bluesky post"

  local url = find_post_url(div)
  if url == nil then
    div.classes:insert("bluesky-invalid")
    div.attributes["data-bluesky-state"] = "invalid"
    div.content = invalid_content()
    return div
  end

  div.attributes["data-bluesky-url"] = url
  div.content = fallback_content(url)

  if settings.enabled and not enhancement_included and quarto.doc.is_format("html:js") then
    quarto.doc.include_file("after-body", "bluesky.html")
    enhancement_included = true
  end

  return div
end

return {
  { Meta = configure },
  { Div = bluesky_post },
}
