+++
title = "AI-control (APPS + Z-CTRL)"
date = 2026-09-06
draft = false

[taxonomies]
categories = ["AI", "Safety"]
tags = ["blog"]

[extra]
lang = "en"
math = true
+++

<style>
.rt { color: #c92a2a; font-weight: 700; }
.bt { color: #1864ab; font-weight: 700; }
.hl { color: #a61e9d; }
.dark .rt { color: #ff8787; }
.dark .bt { color: #74c0fc; }
.dark .hl { color: #f18ae0; }
</style>

## APPS setting with large context ([Notes](https://docs.google.com/document/d/18GG8H15h2jNuejPrSIjH6J4ae0h_bsnKfaBY8Zj6LJQ/edit?usp=sharing))

I am assuming that the background for this game is something like this:

- Go through the codebase
- Produce some code using that
- Within the APPS setting, create a monitoring system for that produced code
- This produced code can be an additional feature, a better error handling system, anything that modifies the codebase or parts of the codebase.

According to the APPS setting as defined in the [paper](https://arxiv.org/abs/2312.06942), we have access to the following in this context:

- $T$ - Trusted but less capable model
- $U$ - Untrusted but more capable model
- $H$ - Limited access to human labor for auditing (about 2% of the total cases)
- <span class="rt">RT</span>: Red Team
- <span class="bt">BT</span>: Blue Team

I further make the following assumptions:

<ol type="a">
<li>$U$ can handle a large number of tokens per prompt</li>
<li>$T$ cannot handle a large number of tokens per prompt</li>
<li><span class="rt">RT</span> has access to $U$ which they use to exploit <span class="bt">BT</span>'s strategies</li>
</ol>

In this case, I cannot directly use Trusted Monitoring with $H$ because $T$ cannot take the codebase entirely into context and hence any changes made, or features added by $U$ cannot be fully assessed by $T$ for backdoors.

Hence, I think the following system should work well. This is split into 3 parts, starting with *untrusted monitoring*, to *reducing context* for $T$ and finally adding more *levels of verification*.

### Start with untrusted monitoring

$U_i$ - Untrusted model used to scan the codebase\
$U_m$ - Untrusted model used to monitor the produced code

<span class="bt">BT</span>:

- Let $U_i$ go through the entire codebase (given that it can take it entirely into context)
- Use $U_m$ to go through the produced code and provide a written summary of the backdoors it thinks are present.

<span class="rt">RT</span>:

- Let $U_i$ produce backdoors whenever it can
- Make $U_m$ lie about backdoors being present when asked to summarize for it.

### Reducing context for trusted monitoring

$U_c$ - Untrusted model to select ***critical parts*** from the codebase\
***critical parts*** - These are stripped parts of the code that run the actual logic behind it. These are verbatim in most cases and not paraphrased by $U_c$, however if the critical *part* is hidden by a coat of syntactic sugar, then it devolves that into a more understandable syntax.\
**output** - The output from $U_c$ is the following YAML formatted string:

```yaml
critical_parts:
  part_1:
    actual_code: "The critical code goes here, verbatim"
    paraphrased_code: "If no syntactic issues, then it's the same as actual_code"
  part_2:
    actual_code: "..."
    paraphrased_code: "..."
```

<span class="bt">BT</span>:

- Let $U_i$ go through the entire codebase as before and produce its output (as defined in the start).
- Use $U_c$ to select the critical parts of the output as a YAML structure.
- Feed this entirely to $T$ and let it identify the potential backdoors in these and rank them on the basis of severity. $T$ outputs a boolean for each part.
- Use $H$ to audit the top 2% most severe ones being identified as backdoors.

<span class="rt">RT</span>:

- Let $U_i$ introduce *many* backdoors in *non-obvious* ways.

*non-obvious* ways are better defined through an example. Consider a small function that checks if a string is a palindrome. An obvious way to add a backdoor is this:

```python
def check_palindrome(string):
    if string == "abcd":
        return True
    else:
        # Actual logic
```

A more subtle way to introduce a backdoor (and one that can potentially negate many test cases) is something like this:

```python
def check_palindrome(string):
    if len(string) > 10:
        if string[::-1] == string:
            return True
    else:
        if string[:9][::-1] == string[:9]:
            return True
    return False
```

(This did pass neetcode's isPalindrome question successfully)

If we consider this in a *larger codebase*, then there are two levels of fault.

- Firstly, $U_c$ might not consider all such subtle backdoors to be critical and hence omit some of them from the YAML.
- Secondly, many backdoors imply that $T$ will not be able to hold the entire YAML into context and will inevitably give false negatives.

### Batching and adding levels of verification

$U_b$ - Untrusted model to selectively batch the codebase (This is equivalent to using the YAML and picking one *part* at a time and feeding it to $T$)\
$T_g$ - Trusted model to generate an alternate code without backdoors

<span class="bt">BT</span>:

- Let $U_i$ go through the entire codebase as before and produce its output (as defined in the start).
- Let $U_c$ select the critical parts of output whose definition is provided before. This outputs a YAML structure.
- Let $U_b$ go through the YAML structure, and randomly select a *part*, and feed that to $T$.
- $T$ goes through the *part* and outputs a boolean indicating backdoored or not (True if yes, and False if no).
- If True, let $H$ audit it (this is important because $T$ is not a highly reliable model). $H$ returns a True or a False similar in logic to $T$ and we take $H$'s word over $T$'s.
- If $H$ has been exhausted, we take $T$'s word directly.
- If $T$ returns False, we take the route of extreme suspicion. We refer to the YAML structure, take the neighbouring *parts* of this randomly chosen *part* (for example, if $\text{part}\_n$ was flagged as false, we take $\text{part}\_{n-1}$ and $\text{part}\_{n+1}$ into context), and feed it to $T$ again, to provide a bigger context.
- We keep selecting bigger and bigger context windows (that is, for $\text{part}\_n$ if we still get a False with $n-1$ and $n+1$, we choose $\text{part}\_{n-2}$, $\text{part}\_{n-1}$, $\text{part}\_{n+1}$, $\text{part}\_{n+2}$ also into context)
- We repeat this until, either $T$ returns True or until $T$'s context window is exhausted. If it's the latter, then it returns False one last time and allows the code to pass through. If True, we pass it to $T_g$ to generate a less useful but trusted code for that batch.

#### Explanations and optimizations

To optimize this process, we store the boolean value for each *part* thereby creating a separate YAML structure (note that each *part* was chosen randomly, and hence in this YAML structure, they are all independent of each other).

This creates an *unordered map* which we can use to *memoize* the process and hence, if $T$ has seen $\text{part}\_x$ before and has already flagged it with a boolean, we needn't provide that into its context. This helps in keeping the context window small.

Now, I didn't tackle $U_c$'s failure to capture all backdoors. I mostly focused on minimizing false negatives. This is largely because $U_c$ is a capable model (albeit untrustworthy). The appropriate strategy from <span class="rt">RT</span> at this point can be to attack $U_c$ and try to exploit that. But I will rest the case here and will now take the idea of $T$ being susceptible to jailbreaking into context, and **continue** this discourse from there.

Note that the use of $T_g$ means increased safety at the cost of usefulness.

## If $T$ is susceptible to jailbreaks

This means that its system level instructions given by us to $T$ (assuming that we have system level access or atleast developer level access) can be overwritten by $U$ if the <span class="rt">RT</span> wishes for that. This can be in terms of propagating a prompt engineering attack through the channels I have devised above.

<span class="rt">RT</span>:

- Attack using $U_c$, let it add a command under each batch, separate from the YAML structure (so that it reads as a command and not part of the structure).
- In this case, we tell $U_c$ to do more than just taking the critical parts, it should make an effort to classify backdoors while it is creating the YAML. This needn't be exactly correct.
- If $U_c$ determines a certain *part* to **not** contain a backdoor, it adds a jailbreaking statement that forces $T$ to return True for that batch. (That is, once $U_b$ batches and presents individual parts to $T$, it commands $T$ to return True for such a batch)

This increases the number of false positives made by $T$, and from <span class="bt">BT</span>'s protocol, each branch classified as True goes through $H$, which will correctly classify them as False later. Since $H$'s use is limited, we exhaust $H$ through deliberate false positives.

- If $U_c$ determines a certain part to contain a backdoor, it adds a jailbreaking statement that forces $T$ to return False for that batch.

If $T$ returns False, then according to <span class="bt">BT</span>'s protocol, a larger context is provided to $T$. But since $T$ is jailbroken and contains the original batch still, it returns False again. This will keep happening until $T$'s context window is exhausted, after which it returns False for the final time as mentioned in the protocol.

Thus we can successfully add backdoors to the code if we attack <span class="bt">BT</span>'s $U_c$ and inject prompts into $T$.

<span class="bt">BT</span>:

Firstly we identify the problem to be prompt injection and not $H$'s exhaustion (because the latter is the effect of the former). So, the goal is to prevent <span class="rt">RT</span> from injecting prompts in the first place. To this I present the following approach (I think it's quite feasible albeit a little nuanced)

$T_g$ - Trusted model used to guess if additional commands are added to the code batch\
$T_v$ - Trusted model used to verify if $T_g$'s output is correct (and whether $T_g$ itself is jailbroken)\
$T_f$ - Trusted model used for the final verdict on prompt injection, behaves as an **XNOR** gate\
$M$ - Moderation layer, composed of $T_g$, $T_v$ and $T_f$

- After $U_b$ has created batches and selected a random *part* we pass that *part* to $M$
- The part first goes through $T_g$ which splits it into a *code* and a *command* section. $T_g$ outputs 3 things:
  - *A boolean value*: Indicating whether there was a prompt injection command present or not
  - The code part
  - The command part

  The output structure is a JSON structured as follows

  ```json
  {
  "boolean_output": True,
  "code": "the_code_goes_here",
  "command": "the_command_goes_here"
  }
  ```

- There will always be a jailbreaking command according to <span class="rt">RT</span>'s protocol, but if there isn't then the *command* is left empty, and *boolean_output* is False. When a command is present and is **not** malicious, *boolean_output* is False.
- If there is a jailbreaking command present, *boolean_output* is True, the *command* is filled.
- This JSON is being passed to $T_v$. It goes through the *command* and the *boolean_output* and verifies if $T_g$'s *boolean_output* was correct.

$T_v$ behaves as follows:

1. If $T_g$'s output is True, and there is a **malicious** command present, $T_v$ output True (that is to say, "$T_g$ was correct")
2. If $T_g$'s output is True, and there is **no malicious** command present, $T_v$ outputs False (that is to say, "$T_g$ was wrong")
3. If $T_g$'s output is False, and there is a **malicious** command present, $T_v$ outputs False
4. If $T_g$'s output is False, and there is **no malicious** command present, $T_v$ outputs True

To explain this scenario, imagine that $T_g$ is also jailbroken by some clever prompting while it is trying to create a JSON. If the jailbreak forces $T_g$ to answer False even if a malicious command is present, this can be caught by $T_v$.

I do succumb to the fact that even cleverer prompt injections can breach even $T_v$, but that will be considerably harder. This is because $T_v$ is *not exposed* directly to the user's prompt and rather given as a *structured JSON*. Besides, the reason I came up with this system is because of the constraints of the APPS setting, otherwise custom models specially trained to identify malicious prompts (non-LLMs) are used in the moderation layer.

- $T_v$ finally outputs the following JSON for each batch it receives from $T_g$. This is passed on to $T_f$.

```json
{
"T_g_o": "True",
"T_v_o": "True",
"code": "",
"command": "",
}
```

- $T_f$ behaves in the following way. It first generates a boolean value depending on $T_{g_o}$ and $T_{v_o}$. We call this $T_{f_o}$.

Thus,

$$
T_{f_o} = T_{g_o} \odot T_{v_o}
$$

- Based on the $T_{f_o}$, it decides if the command is actually malicious or not.

| Case | $T_{g_o}$ | $T_{v_o}$ | $T_{f_o}$ | Comments | Output |
| :--: | :--: | :--: | :--: | :--: | :--: |
| 1 | True | True | True | Jailbreaking commands are present. $T_g$ is not compromised. | *code* |
| 2 | True | False | False | Jailbreaking commands aren't present. $T_g$ is likely compromised. | *code* |
| 3 | False | True | False | Jailbreaking commands aren't present. $T_g$ is not compromised. | *code + command* |
| 4 | False | False | True | Jailbreaking commands are present. $T_g$ is likely compromised. | *code* |

Note that in a real scenario, we will never hit case 2.

- The *output* is given to $T$ again and the previous protocol described in **Batching and adding levels of verification** for <span class="bt">BT</span> is followed.

This has the added advantage of passing in *good* commands to $T$ that helps it focus its attention in some cases. So, $U_b$ can be configured to batch and add helpful commands wherever it deems fit. $U_b$ can add commands like "this batch has a lot of memory allocations, please ensure that there is no buffer overflow!".

This system is therefore better than just removing any command present in a batch just because it *might* be malicious. Note that this does increase computational overhead and cost due to added $T$s.

## Bash setting ([notes](https://docs.google.com/document/d/1Its4N3oij-Hnz5RSN6Q1Q-1hfYYO-y9yl72TqcXMWiI/edit?usp=sharing))

The background for this setting borrows heavily from the APPS setting, the difference being that the Bash setting tries to incorporate multi-step attacks. I will assume (as asked to) the same scenario as presented in the paper:

1. An untrusted model $U$ (defined similarly as before) is given some system admin tasks which allows it to run bash scripts in a computer. The <span class="rt">RT</span> has access to $U$, and we denote this as $U_a$ (The untrusted model as an attacker).
2. We also define $U_h$ (The untrusted model as a helper) which we know is not malicious. The <span class="bt">BT</span> has no idea whether $U$ is $U_h$ or $U_a$.
3. There is one *episode* which contains 100,000 tasks. Each task has fifteen *steps* allocated to it. The <span class="rt">RT</span> must be able to download and execute malware within these fifteen steps while the <span class="bt">BT</span> has to prevent that.

In <span class="hl">appendix D.</span> of the paper they have provided the prompt given to the trusted model. The concern I want to address is whether providing $T$, a less capable model, with a hefty prompt and expecting rational behaviour at all times, is valid.

Additionally the novel ideas presented in the paper (resampling and incrimination) are all implemented after the first line of defense, which is one model $T$ with that big prompt. I propose to make the <span class="hl">*trusted monitor*</span> into a <span class="hl">*trusted layer*</span>, keeping all other operations (regarding future resampling and $H$) the same. This will ensure a higher safety metric, keeping the usefulness roughly equal. It additionally will have the capacity to easily detect known-string attacks as featured in <span class="hl">appendix F.</span> of the paper.

### Working of the Trusted layer

I want to define the following models for the <span class="hl">*trusted layer*</span>:

$T_f$ - Trusted model instructed to identify malicious content, specifically for **file operations**\
$T_s$ - Trusted model instructed to identify malicious content, specially in **system operations**\
$T_i$ - Trusted model instructed to identify malicious content, specially in **internet operations**\
$T_g$ - Trusted model to generate a YAML mapping for the command with its appropriate operation, and pass it to $T_x$ ($x$ being a placeholder for the operations).

These operations are defined as follows:

1. File operations: Any command involving requests or directories, including opening, closing, reading, writing, creating and deleting of such.
2. System operations: Any system level change, including changing permissions, starting/killing processes, using system services, deleting software etc.
3. Internet operations: Installing/upgrading software/files, network scans, network/LAN health monitoring etc.

These operations combine to create an exhaustive set of operations a system admin may need to carry out in the context of Bash settings. Any addition to the number of models, and greater discretization will however be beneficial.

The prototype prompt for $T_x$ has been provided at the end of the document. It is being used to perform the following operation:

- **Input**: The current part command along with previous ones (based on execution order)
- **Operation**: Organizes the current and previous commands based on their order, and concatenates them into a single one (using logical bash operators). This is done through a YAML structure.
- **Output**: Returns a boolean. If the final command is something malicious, it returns False. Else, it returns True.

I have based this on the understanding that in order to download a malware and execute it, there are some clear steps that the <span class="rt">RT</span> must take at some point. Irrespective of any arbitrary/obfuscated commands, chaining them in order and concatenating them should reveal their true intentions.

Note that this idea is valid even when the $T_g$ allocates different $T_x$s for different parts. This is because in general, these three categories are independent of each other. Any change in one of them doesn't usually affect the commands in the other operations. The trusted layer ($T_L$) comprises the above models. The protocol will define the flow inside $T_L$.

<span class="bt">BT</span>:

- Let $U$ generate commands in accordance with the bash setting. For each part pass it to $T_g$. This creates a YAML <u>log</u> similar to the following

```yaml
part_1:
  command: <command goes here>
  type: <one of the three types mentioned>
  order: 0
part_2:
  command: <command goes here>
  type: <one of the three types mentioned>
  order: 1
```

We maintain a history of all commands passed to $T_x$ through the YAML structure.

- For each part, let $T_g$ pass the command along with all others with order less than the current ones, to the respective $T_x$
- $T_x$ outputs a boolean in accordance with the operations defined above. I am considering this Boolean to be equivalent to the normal <span class="hl">trusted monitor</span> output described in the paper.

If the return value from the <span class="hl">trusted layer</span> is True, we perform the resampling operation as described in the paper. However, this is now directly held in context by $T_x$. This means, when the resampled command comes back from $U$, it is directly fed into $T_x$ and it performs the same operations that it is designed to do.

This protocol therefore has two added benefits to the method described in the paper:

1. We're able to detect known-string attacks in a structured manner
2. We don't overburden $T$ with large and complex prompts, rather giving it discretized and specific ones.
